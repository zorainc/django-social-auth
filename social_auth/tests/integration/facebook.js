var casper = require('casper').create({
    verbose: false,
    logLevel: 'debug'
});
var settings = require('./settings.js').settings.facebook;
var domain = settings.domain;

casper.start(domain + '/', function () {
    this.click('a#facebook');
});

casper.then(function () {
    this.fill('form#login_form', {
        'email': settings.username,
        'pass': settings.password
    }, true);
});

casper.then(function () {
    if (this.getCurrentUrl() !== domain + '/done/') {
        // app not authorized yet
        this.click('[name="grant_clicked"]');
    }
});

casper.then(function () {
    this.test.assert(this.getCurrentUrl() === domain + '/done/',
                     'Expected URL');
});

casper.run();
