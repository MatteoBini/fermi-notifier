const calendarId = "isfermimantova@gmail.com"


let step;


let range = {
  start: {
    column: "A",
    line: 2,
  },
  end: {
    column: "I",
    line: 0
  }
};


function getYesterday() {
  const today = new Date();
  const yesterday = new Date(new Date().setDate(today.getDate() - 1));
  return yesterday.toISOString();
}
function getTomorrow() {
  const today = new Date();  
  const tomorrow = new Date(new Date().setDate(today.getDate() + 3));
  return tomorrow.toISOString();
}


const optionalArgs = {
  timeMin: getYesterday(),
  timeMax: getTomorrow(),
  showDeleted: false,
  singleEvents: true,
  orderBy: 'startTime'
}


function listUpcomingEvents() {
  /**
   * Executed automatically every 5 minutes.
   * Loads the events from google calendar in
   * the table.
   */
  const events = Calendar.Events.list(calendarId, optionalArgs).items;
  step = events.length;
  const basicEvents = events.map(event => [
    event.id,
    event.summary,
    event.description,
    event.start.date,
    event.start.dateTime,
    event.start.timeZone,
    event.end.date,
    event.end.dateTime,
    event.end.timeZone
  ]);
  SpreadsheetApp.getActiveSpreadsheet().getRange(getRangeString()).setValues(basicEvents);
  return;
}


function getRangeString() {
  /**
   * Does string operations
   * Returns the string of the range of the content do be 
   * written (without overwrite the old content).
   */
  // set range
  range.end.line = step + 1;

  // range string
  let r = "";
  r = r + range.start.column;         // always "A"
  r = r + range.start.line;           // variable
  r = r + ":";                        // to separe limits
  r = r + range.end.column;           // always "H"
  r = r + range.end.line;             // variable

  // moving range
  range.start.line = range.start.line + step;
  range.end.line = range.end.line + step;

  return r;
}


function isoToDate(dateISOStr) {
  /**
   * Return a Date object from a ISO string
   */
  let str = dateISOStr.replace(/-/,'/').replace(/-/,'/').replace(/T/,' ').replace(/\+/,' \+').replace(/Z/,' +00');
  return new Date(str);
}


function removeOldEvents() {
  /**
   * Removes from the spreadsheet the events before yesterday analyzing the
   * time of the elements of the first 500 lines. 
   */
  var data = SpreadsheetApp.getActiveSheet().getRange("G1:H500").getValues();

  for(let i=1; i<500; i++){
    if(data[i][0] != ""){
      if(isoToDate(data[i][0]).valueOf() < isoToDate(getYesterday()).valueOf()){
        SpreadsheetApp.getActiveSheet().deleteRow(i+1);
      }
    }else{
      if(isoToDate(data[i][1]).valueOf() < isoToDate(getYesterday()).valueOf()){
        SpreadsheetApp.getActiveSheet().deleteRow(i+1);
      }
    }
  }
  
  return;
}
