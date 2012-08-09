var settings = require('./settings.js').settings,
    provider = settings.twitter || {},
    domain,
    casper;

// Run only if there are credentias
if (provider.username && provider.password) {
    domain = provider.domain || settings.domain;
    casper = require('casper').create(settings.casper);

    casper.start(domain + '/', function () {
        this.click(provider.linkSelector);
    });

    casper.then(function () {
        this.fill('form#oauth_form', {
            'session[username_or_email]': provider.username,
            'session[password]': provider.password
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
}
