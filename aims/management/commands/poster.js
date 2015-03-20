/* source: http://stackoverflow.com/questions/9246438/how-to-submit-a-form-using-phantomjs */

system = require('system')
if (system.args.length < 3 || system.args.length > 5) {
    console.log('Usage: poster.js URL filename [paperwidth*paperheight|paperformat] [zoom]');
    console.log('  paper (pdf output) examples: "5in*7.5in", "10cm*20cm", "A4", "Letter"');
    phantom.exit(1);
}
var page = new WebPage(), testindex = 0, loadInProgress = false;
if (system.args.length > 3 && system.args[2].substr(-4) === ".pdf") {
    size = system.args[3].split('*');
    page.paperSize = size.length === 2 ? { width: size[0], height: size[1], margin: '0px' }
        : { format: system.args[3], orientation: 'landscape', margin: '1cm' };
}

address = system.args[1];
output = system.args[2];
console.log(address)
console.log(output)

page.viewportSize = { width: 1000, height: 1000 };

page.onConsoleMessage = function(msg) {
  console.log(msg);
};

page.onLoadStarted = function() {
  loadInProgress = true;
  console.log("load started");
};

page.onLoadFinished = function() {
  loadInProgress = false;
  console.log("load finished");
};

var steps = [
  function() {
    //Load Login Page
    page.open(address);
//    page.open("http://127.0.0.1:8000/");
  },
  function() {
    //Enter Credentials
    page.evaluate(function() {

      var arr = document.getElementsByClassName("form-signin");
      var i;

      for (i=0; i < arr.length; i++) { 
        if (arr[i].getAttribute('method') == "POST") {
          arr[i].elements["username"].value="ders";
          arr[i].elements["password"].value="mhuire";
          return;
        }
      }
    });
  }, 
  function() {
    //Login
    page.evaluate(function() {
      var arr = document.getElementsByClassName("form-signin");
      var i;

      for (i=0; i < arr.length; i++) {
        if (arr[i].getAttribute('method') == "POST") {
          arr[i].submit();
          return;
        }
      }
    });
  }, 
  function() {
      page.render(output);
      phantom.exit();
  }
];


interval = setInterval(function() {
  if (!loadInProgress && typeof steps[testindex] == "function") {
    console.log("step " + (testindex + 1));
    steps[testindex]();
    testindex++;
  }
  if (typeof steps[testindex] != "function") {
    console.log("test complete!");
    phantom.exit();
  }
}, 50);