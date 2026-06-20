document.addEventListener('DOMContentLoaded', () => {
    const copyElements = document.querySelectorAll('.copyable-text');
    const announcer = document.getElementById('copy-announcer');
    const toast = document.getElementById('toast');

    let toastTimeout;
    let announcerTimeout;

    copyElements.forEach(el => {
        let bgTimeout;

        const handleCopy = () => {
            const textToCopy = el.textContent;
            navigator.clipboard.writeText(textToCopy).then(() => {
                // Clear existing timeouts
                clearTimeout(bgTimeout);
                clearTimeout(toastTimeout);
                clearTimeout(announcerTimeout);

                // Clear native text selection so success background is visible
                window.getSelection().removeAllRanges();

                // Visual feedback (inline)
                el.classList.remove('copy-error');
                el.classList.add('copy-success');
                if (!el.hasAttribute('data-original-title')) {
                    const originalTitle = el.getAttribute('title');
                    if (originalTitle) {
                        el.setAttribute('data-original-title', originalTitle);
                    } else {
                        el.setAttribute('data-original-title', '');
                    }
                }
                el.setAttribute('title', 'Copied!');

                // Visual feedback (toast)
                toast.textContent = `Copied ${textToCopy} to clipboard!`;
                toast.classList.remove('copy-error');
                toast.classList.add('show');

                // Auditory feedback
                announcer.textContent = `Copied ${textToCopy} to clipboard`;

                bgTimeout = setTimeout(() => {
                    el.classList.remove('copy-success');
                    const originalTitle = el.getAttribute('data-original-title');
                    if (originalTitle) {
                        el.setAttribute('title', originalTitle);
                    } else {
                        el.removeAttribute('title');
                    }
                    el.removeAttribute('data-original-title');
                }, 2000);

                toastTimeout = setTimeout(() => {
                    toast.classList.remove('show');
                    // Clear announcer after a delay so it doesn't read out old messages if focused later
                    announcerTimeout = setTimeout(() => announcer.textContent = '', 1000);
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy text: ', err);

                // Clear existing timeouts
                clearTimeout(bgTimeout);
                clearTimeout(toastTimeout);
                clearTimeout(announcerTimeout);

                // Visual feedback (inline)
                el.classList.remove('copy-success');
                el.classList.add('copy-error');
                if (!el.hasAttribute('data-original-title')) {
                    const originalTitle = el.getAttribute('title');
                    if (originalTitle) {
                        el.setAttribute('data-original-title', originalTitle);
                    } else {
                        el.setAttribute('data-original-title', '');
                    }
                }
                el.setAttribute('title', 'Failed to copy!');

                // Visual feedback (toast)
                toast.textContent = 'Failed to copy to clipboard';
                toast.classList.add('copy-error');
                toast.classList.add('show');

                // Auditory feedback
                announcer.textContent = 'Failed to copy to clipboard';

                bgTimeout = setTimeout(() => {
                    el.classList.remove('copy-error');
                    const originalTitle = el.getAttribute('data-original-title');
                    if (originalTitle) {
                        el.setAttribute('title', originalTitle);
                    } else {
                        el.removeAttribute('title');
                    }
                    el.removeAttribute('data-original-title');
                }, 2000);

                toastTimeout = setTimeout(() => {
                    toast.classList.remove('show');
                    toast.classList.remove('copy-error');
                    // Clear announcer after a delay
                    announcerTimeout = setTimeout(() => announcer.textContent = '', 1000);
                }, 2000);
            });
        };

        el.addEventListener('click', handleCopy);

        el.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault(); // Prevent scrolling on space
                handleCopy();
            }
        });
    });
});
