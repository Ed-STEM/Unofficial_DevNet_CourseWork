//sizing variables
const sidebar_width_collapsed = '70px'
const sidebar_width_opened = '210px'
const sidebar_height = '100%'
const main_width = '95%'
const main_height = '100%'

//color variables
const text_white = '#FDFEFE'
const text_teal = '#8BD8BD'
const bkgd_light_purple = '#6666ff'
const bkgd_dark_purple = '#2F3C7E'
const bkgd_purple = '#7a52ba'
const bkgd_baige = '#FBEAEB'

//padding variables 
const top_lvl_radius = '8px'
const container_radius = '4px'

//Sidebar open and close functions.
function changeSideNav() {
    if (document.querySelector('.sidebar').style.width == sidebar_width_collapsed)
    {
        document.querySelector('.sidebar').style.width = sidebar_width_opened
        document.querySelector('.content').style.marginLeft = sidebar_width_opened
        try{
        document.querySelector('.content_header').style.marginLeft = sidebar_width_opened
        } catch(err) {
            console.log(err)
        } finally {
        const sidebar_list = document.querySelectorAll('.sidebar_text');
        for (let i = 0; i < sidebar_list.length; i++ ){
            sidebar_list[i].style.visibility = 'visible';
        }
    }

    } else {
        document.querySelector('.sidebar').style.width = sidebar_width_collapsed
        document.querySelector('.content').style.marginLeft = sidebar_width_collapsed
        try{
        document.querySelector('.content_header').style.marginLeft = sidebar_width_collapsed
        } catch(err){
            console.log(err)
        } finally {
        const sidebar_list2 = document.querySelectorAll('.sidebar_text');
        for (let i = 0; i < sidebar_list2.length; i++ ){
            sidebar_list2[i].style.visibility = 'hidden';
        }
    }
    }
}



//Webex integration referece:  https://developer.webex.com/docs/embedded-apps-api-reference
//var app = new window.Webex.Application();

app.onReady().then(function () {
  console.log('App is ready. App info:', app);
});