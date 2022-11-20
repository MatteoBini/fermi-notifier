const toggleButton = document.getElementsByClassName('hamburger')[0];
const navLinks = document.getElementsByClassName('nav-links')[0];
var ul = navLinks.getElementsByTagName('ul')[0];

toggleButton.addEventListener('click', () => {
    if(navLinks.classList.contains('active')){
        


        for(let i = 0; i < ul.getElementsByTagName('li').length; i++){
            setTimeout(() => {
                ul.getElementsByTagName('li')[ul.getElementsByTagName('li').length - i - 1].classList.add('li-inactive');
                ul.getElementsByTagName('li')[ul.getElementsByTagName('li').length - i - 1].classList.remove('li-active');
                ul.getElementsByTagName('li')[ul.getElementsByTagName('li').length - i - 1].style.visibility = 'hidden';
            }, 250 * i);
        }
        
        setTimeout(() => {
            navLinks.classList.remove('active');
            navLinks.classList.add('inactive');
        }, 250 * ul.getElementsByTagName('li').length);

        for (var i = 0; i < toggleButton.children.length; i++) {
            toggleButton.children[i].classList.remove('line-pazzo');
        }

    }else{
        navLinks.classList.remove('inactive');
        navLinks.classList.add('active');

        for (var i = 0; i < toggleButton.children.length; i++) {
            toggleButton.children[i].classList.add('line-pazzo');
        }

        for(let i = 0; i < ul.getElementsByTagName('li').length; i++){
            setTimeout(() => {
                ul.getElementsByTagName('li')[i].classList.remove('li-inactive');
                ul.getElementsByTagName('li')[i].classList.add('li-active');
                ul.getElementsByTagName('li')[i].style.visibility = 'visible';
            }, 250 * i);
        }
    }
})