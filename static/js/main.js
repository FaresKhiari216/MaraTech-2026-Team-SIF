(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner(0);
    
    
    // Initiate the wowjs
    new WOW().init();


    // Fixed Navbar
    $(window).scroll(function () {
        if ($(window).width() < 992) {
            if ($(this).scrollTop() > 45) {
                $('.fixed-top').addClass('bg-white shadow');
            } else {
                $('.fixed-top').removeClass('bg-white shadow');
            }
        } else {
            if ($(this).scrollTop() > 45) {
                $('.fixed-top').addClass('bg-white shadow').css('top', -45);
            } else {
                $('.fixed-top').removeClass('bg-white shadow').css('top', 0);
            }
        }
    });
    
    
   // Back to top button
   $(window).scroll(function () {
    if ($(this).scrollTop() > 300) {
        $('.back-to-top').fadeIn('slow');
    } else {
        $('.back-to-top').fadeOut('slow');
    }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Testimonial carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1500,
        dots: false,
        loop: true,
        margin: 25,
        nav : true,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ],
        responsive: {
            0:{
                items:1
            },
            768:{
                items:1
            },
            992:{
                items:2
            },
            1200:{
                items:3
            }
        }
    });


    // Dark mode toggle
    const themeKey = 'site-theme';
    const $body = $('body');
    const $darkToggle = $('#darkModeToggle');

    function applyTheme(theme) {
        if (theme === 'dark') {
            $body.addClass('dark-mode');
            if ($darkToggle.length) {
                $darkToggle.prop('checked', true);
            }
        } else {
            $body.removeClass('dark-mode');
            if ($darkToggle.length) {
                $darkToggle.prop('checked', false);
            }
        }
    }

    // Initial theme from localStorage
    const storedTheme = localStorage.getItem(themeKey);
    if (storedTheme === 'dark' || storedTheme === 'light') {
        applyTheme(storedTheme);
    }

    // If no preference stored, keep light by default

    if ($darkToggle.length) {
        $darkToggle.on('change', function () {
            const newTheme = $(this).is(':checked') ? 'dark' : 'light';
            localStorage.setItem(themeKey, newTheme);
            applyTheme(newTheme);
        });
    }

    // Text-to-speech (lecture audio)
    const ttsKey = 'site-tts';
    const $ttsToggle = $('#ttsToggle');

    function isTtsSupported() {
        return 'speechSynthesis' in window && 'SpeechSynthesisUtterance' in window;
    }

    function speakText(text) {
        if (!isTtsSupported() || !text) return;
        try {
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'fr-FR';
            window.speechSynthesis.speak(utterance);
        } catch (e) {
            // Fail silently if TTS is blocked by the browser
        }
    }

    function setTtsEnabled(enabled) {
        if (!isTtsSupported()) return;
        localStorage.setItem(ttsKey, enabled ? 'on' : 'off');
        if ($ttsToggle.length) {
            $ttsToggle.prop('checked', enabled);
            $ttsToggle.attr('aria-pressed', enabled ? 'true' : 'false');
        }
    }

    function getElementTextForTts($el) {
        const dataText = $el.data('tts');
        const ariaLabel = $el.attr('aria-label');
        const visibleText = $el.text();
        const raw = dataText || ariaLabel || visibleText;
        if (!raw) return '';
        return raw.replace(/\s+/g, ' ').trim();
    }

    if (isTtsSupported()) {
        const storedTts = localStorage.getItem(ttsKey);
        const initialEnabled = storedTts === 'on';

        if ($ttsToggle.length) {
            $ttsToggle.prop('disabled', false);
            setTtsEnabled(initialEnabled);
            $ttsToggle.on('change', function () {
                setTtsEnabled($(this).is(':checked'));
            });
        }

        function isTtsEnabled() {
            return localStorage.getItem(ttsKey) === 'on';
        }

        // Read on click for buttons, nav links, labels, headings, and description texts
        $(document).on('click', function (event) {
            if (!isTtsEnabled()) return;
            const $target = $(event.target);
            const $speakEl = $target.closest('button, [role="button"], a.btn, .btn, a.nav-link, label, [data-tts], h1, h2, h3, h4, h5, h6, .description-text');
            if (!$speakEl.length) return;
            const text = getElementTextForTts($speakEl);
            if (text) {
                speakText(text);
            }
        });

        // Read on keyboard focus for interactive elements and description texts
        $(document).on('focusin', 'button, [role="button"], a.btn, .btn, a.nav-link, label, [data-tts], .description-text', function () {
            if (!isTtsEnabled()) return;
            const $el = $(this);
            const text = getElementTextForTts($el);
            if (text) {
                speakText(text);
            }
        });
    } else {
        if ($ttsToggle.length) {
            $ttsToggle.prop('disabled', true);
            $ttsToggle.attr('aria-disabled', 'true');
        }
    }

    // Info-bulles globales (tooltips) pour tout le site
    function getElementTextForTooltip($el) {
        // Ne pas générer pour html/body/script/style
        const tag = ($el.prop('tagName') || '').toLowerCase();
        if (!tag || tag === 'html' || tag === 'body' || tag === 'script' || tag === 'style') {
            return '';
        }

        const ariaLabel = $el.attr('aria-label');
        const placeholder = $el.attr('placeholder');
        const alt = $el.attr('alt');
        const text = ariaLabel || placeholder || alt || $el.text();
        if (!text) return '';
        const cleaned = text.replace(/\s+/g, ' ').trim();

        // Préfixes en fonction du type d'élément
        const role = ($el.attr('role') || '').toLowerCase();
        const type = ($el.attr('type') || '').toLowerCase();
        let prefix = '';

        const lowerText = cleaned.toLowerCase();

        // Boutons (vrais boutons, liens bouton, éléments avec rôle bouton)
        if (tag === 'button' || role === 'button' || $el.hasClass('btn') || (tag === 'input' && (type === 'button' || type === 'submit' || type === 'reset'))) {
            prefix = 'bouton - ';
        }
        // Filtres / champs de formulaire
        else if (tag === 'input' || tag === 'select' || tag === 'textarea') {
            prefix = 'filtre - ';
        }
        // Logo (image de marque, alt ou texte contenant logo ou nom du site)
        else if (tag === 'img' && (lowerText.includes('logo') || (alt && alt.toLowerCase().includes('logo')))) {
            prefix = 'logo - ';
        }
        // Profil (éléments liés au profil utilisateur)
        else if (lowerText.includes('profil') || lowerText.includes('profile')) {
            prefix = 'profile - ';
        }
        // Annonces (cartes et liens d'annonces)
        else if ($el.closest('.sermon-item').length || lowerText.includes('annonce')) {
            prefix = 'annonce - ';
        }
        // Pages (liens de navigation principaux)
        else if ( lowerText.includes('accueil') || lowerText.includes('Evenement') || lowerText.includes('Cas sociaux') || lowerText.includes('contact') || lowerText.includes('about')) {
            prefix = 'page - ';
        }
        // Événements (listes et cartes d'événements)
        else if ($el.closest('.event-item').length || lowerText.includes('événement')) {
            prefix = 'événement - ';
        }
        // Titre (tout autre titre h1-h6)
        else if (tag === 'h1' || tag === 'h2' || tag === 'h3' || tag === 'h4' || tag === 'h5' || tag === 'h6') {
            // Titre principal de page (h1 dans le main)
            if (tag === 'h1' && $el.closest('main').length) {
                prefix = 'page - ';
            } else {
                prefix = 'titre - ';
            }
        }
        // Lien générique
        else if (tag === 'a') {
            prefix = 'lien - ';
        }
        // Image générique
        else if (tag === 'img') {
            prefix = 'image - ';
        }
        // Sections / conteneurs importants
        else if (tag === 'section' || tag === 'main' || tag === 'nav' || tag === 'header' || tag === 'footer') {
            prefix = 'section - ';
        }

        const full = prefix ? prefix + cleaned : cleaned;
        // Limiter la longueur pour éviter des info-bulles trop longues
        return full.length > 160 ? full.substring(0, 157) + '…' : full;
    }

    // Au survol ou au focus, si pas déjà de title, on en génère un
    $(document).on('mouseenter focusin', '*', function () {
        const $el = $(this);
        if ($el.attr('title')) return; // ne pas écraser les info-bulles existantes
        const tooltipText = getElementTextForTooltip($el);
        if (tooltipText) {
            $el.attr('title', tooltipText);
        }
    });

})(jQuery);

