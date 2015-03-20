$(document).ready(
    function()
    {
   
        var introTour = introJs();
        introTour.setOptions({
            showStepNumbers: false,
            nextLabel: 'Next',
            prevLabel: 'Back',
            exitOnEsc: false,
            exitOnOverlayClick: false,
            showBullets: false,
            tooltipPosition: 'auto',
            scrollToElement: true,
            steps: [
                {
                    intro: '<div class="shepherd-logo"></div><div class="shephered-header">Welcome to Mohinga</div>Mohinga is Myanmar\'s Aid Information Management System (AIMS). The Mohinga application allows development partners to report their assistance to Myanmar in a simple, common, comparable format.<hr/><div class="disclaimer_header text-center hidden-xs">Disclaimer</div> <div class="disclaimer_text hidden-xs">Data contained within Mohinga has been collected in partnership with Myanmar’s development partners as part of an ongoing process of collaboration and dialogue. Before using the data, we encourage all users to first contact the relevant development partners to ensure data is accurate.</div><br/>'
                },
                {
                    intro: '<div class="shephered-subheader">Search within Mohinga</div> Mohinga contains a lot of information. To find what you’re looking for try searching by development partner, activity or sector. <br/><div class="shephered-subheader">Profile pages</div>Each development partner also has a dedicated <strong>profile page</strong> with information on all their activities. You can access their profile pages by searching for their name here.',
                    element: '.navbar .search-bar-main',
                },
                {
                    intro: '<div class="shephered-subheader">Visualise aid flows</div>Mohinga visualises aid flows to Myanmar via four interactive dashboards -- you can see aid by location, donor, sector or Ministry responsible. Click here to access the dashboards.',
                    element: '#navigation-dropdown',
                },
                {
                    intro: '<div class="shephered-subheader">Filtering the dashboard by date</div>The date filter allows you to filter information presented on the dashboards between a specific time period. Select a start and end date and then click the refresh button to set the filter. ',
                    element: '.input-daterange',
                },
                {
                    intro: '<div class="shephered-subheader">Exporting data from Mohinga</div>The export function will download the dashboard data to a .CSV file. Also, if you have set a date range or zoomed into Shan state or selected a specific organisation, clicking export will just give you that data.',
                    element: '.export-csv',
                },
                {
                    intro: '<div class="shephered-subheader">Activity List</div>Data from all of the activities below is used to calculate the figures that appear in the dashboard above. Click on the blue activity number in the Activity List to visit the Activity Profile page and learn more.',
                    element: '.activity_table',
                },
                 {
                    intro: '<div class="shepherd-logo"></div><div class="shephered-header">That is it... for now. </div> If you need any further information look for these help icons  <i class="ion-information-circled dash-info"></i>  and they will provide you with some additional information about Mohinga.<br/><br/>We are also working hard to bring new features and functions to Mohinga. These include advanced reporting tools and better integration with internationally available IATI aid data. As well as other tools to help make the management of aid information simple, time efficient and even enjoyable. We will be in touch.'
                }
            ]
        });

        if ( $( '.dashboard-container' ).length && !$.browser.mobile ) {

            if ( !localStorage.intro_tour ) {

                localStorage.intro_tour = true;
                introTour.start();
            }

            $( '.tutorial-trigger a' ).on( 'click', function(){ introTour.start(); });

        } else {
            $( '.tutorial-trigger' ).hide();
        }
    }
);
