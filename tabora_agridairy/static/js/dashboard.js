/**
 * Tabora Dairy - UI helpers
 * - Auto-dismiss alerts
 * - Mobile sidebar toggle
 * - Active nav highlighting
 */

(function() {
    'use strict';

    function on(el, event, handler) {
        if (!el) return;
        el.addEventListener(event, handler);
    }

    // Auto-dismiss alerts after 5 seconds
    document.querySelectorAll('.alert-dismissible').forEach(function(alert) {
        setTimeout(function() {
            var bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 5000);
    });

    // Sidebar open/close (mobile)
    var openBtn = document.querySelector('[data-sidebar-open]');
    var closeBtns = document.querySelectorAll('[data-sidebar-close]');
    on(openBtn, 'click', function() {
        document.body.classList.add('sidebar-open');
    });
    closeBtns.forEach(function(btn) {
        on(btn, 'click', function() {
            document.body.classList.remove('sidebar-open');
        });
    });

    // Prevent placeholder links
    document.querySelectorAll('[data-disabled-link]').forEach(function(a) {
        on(a, 'click', function(e) { e.preventDefault(); });
    });

    // Active nav link highlighting (exact pathname)
    try {
        var path = window.location.pathname || '';
        document.querySelectorAll('.app-nav__link[href]').forEach(function(a) {
            var href = a.getAttribute('href') || '';
            if (!href || href === '#') return;
            if (href === path || (href !== '/' && path.startsWith(href))) {
                a.classList.add('is-active');
            }
        });
    } catch (e) {
        // ignore
    }
})();
