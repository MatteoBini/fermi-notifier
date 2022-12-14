const express = require("express");
const { pool } = require("./dbConfig");
const bcrypt = require("bcrypt");
const passport = require("passport");
const flash = require("express-flash");
const session = require("express-session");
require("dotenv").config();
const path = require(`path`);
var bodyParser = require('body-parser')

const app = express();
const PORT = process.env.PORT || 3000;

const initializePassport = require("./passportConfig");
initializePassport(passport);

// Parses details from a form
app.use(express.urlencoded({ extended: false }));
app.use(bodyParser.json())

app.set("view engine", "ejs");

app.use(
  session({
    // Key we want to keep secret which will encrypt all of our information
    secret: process.env.SESSION_SECRET,
    // Should we resave our session variables if nothing has changes which we dont
    resave: false,
    // Save empty value if there is no vaue which we do not want to do
    saveUninitialized: false
  })
);
// Funtion inside passport which initializes passport
app.use(passport.initialize());
// Store our variables to be persisted across the whole session. Works with app.use(Session) above
app.use(passport.session());
app.use(flash());

app.set('case sensitive routing', true);

app.get("/", async (req, res) => {
  if (req.isAuthenticated()) {
    res.render("index.ejs", { isLogged: true, user: await getUserName(req.user.email)});
  }else{
    res.render("index.ejs", { isLogged: false });
  }
});

app.get("/register", checkAuthenticated, (req, res) => {
  res.render("register.ejs");
});

app.get("/credits", (req, res) => {
  res.render("credits.ejs", { isLogged: req.isAuthenticated() });
});

app.get("/faq", (req, res) => {
  res.render("faq.ejs", { isLogged: req.isAuthenticated() });
});

app.get("/login", checkAuthenticated, (req, res) => {
  // flash sets a messages variable. passport sets the error message
  if (req.session.flash != undefined){
    console.log(req.session.flash.error);
  }
  res.render("login.ejs");
});

app.get("/dashboard", checkNotAuthenticated, async (req, res) => {
  let name = await getUserName(req.user.email);
  let keywords = await getUserKeywords(req.user.email);
  let telegram = await getUserTelegram(req.user.email);
  let notifications = await getUserNotifications(req.user.email);
  let gender = await getUserGender(req.user.email);
  let notificationPreferences = await getUserNotificationPreferences(req.user.email);

  res.render("dashboard", { 
    user: name,
    keywords: keywords,
    tgun: telegram,
    n_not: notifications,
    gender: gender,
    n_pref: notificationPreferences
  });
});

app.get("/logout", (req, res, next) => {
  req.logout(function(err){
    if (err) { return next(err); }
  });
  res.redirect("/");
});

app.get("/users/register/confirmation/:id", async (req, res, next) => {
  let userId = req.params.id;
  const a = await incrementNumberNotification(userId);
  res.redirect("/login");
});

app.post("/users/register", async (req, res) => {
  let { name, surname, email, password, password2, gender } = req.body;

  let errors = [];

  if (!name || !email || 
      !password || !password2 || 
      !gender) {
    errors.push({ message: "Compila tutti i campi!" });
  }

  if (password.length < 6) {
    errors.push({ message: "La password deve essere almeno 6 caratteri!" });
  }

  if (password !== password2) {
    errors.push({ message: "Le password non corrispondono!" });
  }

  if (errors.length > 0) {
    res.render("register", { errors, name, email, password, password2 });
    return;
  } 

  // If no errors runs as it follows
  hashedPassword = await bcrypt.hash(password, 10);
  telegramTemporaryCode = await getTelegramTemporaryCode();
  pool.query(
    `SELECT * FROM subscribers
      WHERE email = $1`,
    [email],
    (err, results) => {
      if (err) {
        console.log(err);
      }

      if (results.rows.length > 0) {
        return res.render("register", {
          message: "Email gi?? registrata!"
        });
      } else {
        pool.query(
          `INSERT INTO subscribers (name, surname, email, password, notifications, telegram, gender)
              VALUES ($1, $2, $3, $4, $5, $6, $7)
              RETURNING id, password`,
          [name, surname, email, hashedPassword, -2, telegramTemporaryCode, gender],
          (err, results) => {
            if (err) {
              throw err;
            }
            req.flash("success_msg", "Ti abbiamo inviato una mail per confermare l'account! (controlla anche la SPAM)");
            res.redirect("/login");
          }
        );
      }
    }
  );
});

app.post("/notification-preferences", async (req, res) => {
  let option;

  // I use not true because sometimes value can be also None 
  // or undefined
  if(req.body.email == true && req.body.telegram == true)
    option = 3;
  else if(req.body.email == true && req.body.telegram != true)
    option = 2;
  else if(req.body.email != true && req.body.telegram == true) 
    option = 1;
  else if(req.body.email != true && req.body.telegram != true) 
    option = 0;

  pool.query(
    `UPDATE subscribers
      SET notification_preferences = $1
      WHERE email = $2;`,
    [option, req.user.email],
    (err, results) => {
      if (err) {
        console.log(err);
        throw err;
      }
    }
  );
  res.redirect("/dashboard");
});

app.post("/keyword", async function (req, res) {
  /**
   * If the keyword has already been stored,
   * has to be removed.
   * If the keyword is not stored yet,
   * has to be appended.
   */
  let sentKeyword = req.body.keyword;
  let userKeywords = await getUserKeywords(req.user.email);
  
  sentKeyword = sentKeyword.trim(); // remove spaces from start, end

  let occurrences = 0;
  if(userKeywords!=null){
    userKeywords.forEach(kw => {
      if(kw==sentKeyword) {
        occurrences=occurrences+1;
      }
    });
  }

  if(occurrences>0){
    pool.query(
      `UPDATE subscribers
        SET tags = array_remove(tags, $1)
        WHERE email = $2;`,
      [sentKeyword, req.user.email],
      (err, results) => {
        if (err) {
          console.log(err);
          throw err;
        }
      }
    );
  } else {
    pool.query(
      `UPDATE subscribers
        SET tags = array_append(tags, $1)
        WHERE email = $2;`,
      [sentKeyword, req.user.email],
      (err, results) => {
        if (err) {
          console.log(err);
          throw err;
        }
      }
    );
  }

  res.redirect("/dashboard");
});

app.post(
  "/login",
  passport.authenticate("local", {
    successRedirect: "/dashboard",
    failureRedirect: "/login",
    failureFlash: true
  })
);

function checkAuthenticated(req, res, next) {
  if (req.isAuthenticated()) {
    return res.redirect("/dashboard");
  }
  next();
}

function checkNotAuthenticated(req, res, next) {
  if (req.isAuthenticated()) {
    return next();
  }
  res.redirect("/login");
}

async function getTelegramTemporaryCode() {
  /**
   * This function returns the code that
   * the user has to send to my bot on telegram.
   * 
   * When the bot get this code, register the 
   * telegram user id of the sender (my user).
   * 
   * This code is unique for every subscriber,
   * is generated with a $ at its beginning
   * and parts of the hashed email of the user.
   */
  let code = "X";

  code += (Math.random() + 1).toString(36).substring(6); // add random string of 7 char

  /**
   * VALIDATING CODE
   * Check if the code that I've just generated
   * is not yet associated with someone else.
   */
  allCodes = await getAllTelegram();
  if (allCodes != undefined){
    for(let i=0; i<allCodes.length;i++){
      if(allCodes[i] == code) {
        return getTelegramTemporaryCode(email + "LOL");
      }
    }
  }
  return code;
}

async function getUserName(user_email){
  try {
    const RES = await pool.query(
      `SELECT name FROM subscribers
        WHERE email = '${user_email}'`,
    );
    return RES.rows[0].name;
  } catch (err) {
    console.log(err.stack);
  }
}

async function getUserKeywords(user_email){
  try {
    const RES = await pool.query(
      `SELECT tags FROM subscribers
        WHERE email = '${user_email}'`,
    );
    return RES.rows[0].tags;
  } catch (err) {
    console.log(err.stack);
  }
}

async function getAllTelegram() {
  try {
    const RES = await pool.query(
      `SELECT telegram FROM subscribers;`
    );
    return RES.rows[0].telegram;
  } catch (err) {
    console.log(err.stack);
  }
}

async function getUserTelegram(user_email){
  try {
    const RES = await pool.query(
      `SELECT telegram FROM subscribers
        WHERE email = '${user_email}'`
    );
    return RES.rows[0].telegram;
  } catch (err) {
    console.log(err.stack);
  }
}

async function getUserNotifications(user_email){
  try {
    const RES = await pool.query(
      `SELECT notifications FROM subscribers
        WHERE email = '${user_email}'`,
    );
    return RES.rows[0].notifications;
  } catch (err) {
    console.log(err.stack);
  }
}

async function getUserGender(user_email){
  try {
    const RES = await pool.query(
      `SELECT gender FROM subscribers
        WHERE email = '${user_email}'`,
    );
    return RES.rows[0].gender;
  } catch (err) {
    console.log(err.stack);
  }
}

async function getUserNotificationPreferences(user_email) {
  try {
    const RES = await pool.query(
      `SELECT notification_preferences FROM subscribers
        WHERE email = '${user_email}'`,
    );
    return RES.rows[0].notification_preferences;
  } catch (err) {
    console.log(err.stack);
  }
}

async function incrementNumberNotification(telegramId){
  try {
    const RES = await pool.query(
      `UPDATE subscribers
         SET notifications = notifications + 1
       WHERE telegram = '${telegramId}' AND notifications = -1;`
    );
    return RES;
  } catch (err) {
    console.log(err.stack);
  }
}

/* set static folder for css etc */
app.use(express.static(path.join(__dirname, 'public')))

/* set up 404 page (not found) */
/* WARNING: This route has to be the last one!! */
//The 404 Route (ALWAYS Keep this as the last route)
app.get('*', function(req, res){
  res.render("404.ejs");
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});