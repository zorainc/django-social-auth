var settings = require('./settings.js').settings,
    provider = settings['google-openid'] || {},
    domain,
    casper;

// Run only if there are credentias
if (provider.username && provider.password) {
    domain = provider.domain || settings.domain;
    casper = require('casper').create(settings.casper);

    casper.start(domain + '/', function () {
        this.click('a#google');
    });

    casper.then(function () {
        this.fill('form#gaia_loginform', {
            'Email': provider.username,
            'Passwd': provider.password
        }, true);
    });

    casper.then(function () {
        if (this.getCurrentUrl() !== domain + '/done/') {
            // app not authorized yet
            this.click('#approve_button');
        }
    });

    casper.then(function () {
        this.test.assert(this.getCurrentUrl() === domain + '/done/',
                         'Expected URL');
    });

    casper.run();
}
