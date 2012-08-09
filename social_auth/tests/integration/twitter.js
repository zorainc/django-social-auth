var casper = require('casper').create({
    verbose: false,
    logLevel: 'debug'
});
var settings = require('./settings.js').settings;
var domain = settings.facebook.domain;

casper.start(domain + '/', function () {
    this.click('a#twitter');
});

casper.then(function () {
    this.fill('form#oauth_form', {
        'session[username_or_email]': settings.facebook.username,
        'session[password]': settings.facebook.password
    }, true);
});

casper.then(function () {
    if (this.evaluate(function () { return __utils__.exists('input#allow'); })) {
        // app not authorized yet
        this.click('input#allow');
    }
});

casper.then(function () {
    // wait for twitter redirect back to social-auth
    this.waitFor(function () {
        return this.getCurrentUrl().match(new RegExp(domain));
    }, function () {
        this.test.assert(this.getCurrentUrl() === domain + '/done/',
                         'Expected URL');
    });
});

casper.run();
