var settings = require('./settings.js').settings,
    provider = settings.facebook || {},
    domain,
    casper;

// Run only if there are credentias
if (provider.username && provider.password) {
    domain = provider.domain || settings.domain;
    casper = require('casper').create(settings.casper);

    casper.start(domain + '/', function () {
        this.click('a#facebook');
    });

    casper.then(function () {
        this.fill('form#login_form', {
            'email': provider.username,
            'pass': provider.password
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
}
