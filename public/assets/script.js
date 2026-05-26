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

                // Visual feedback (inline)
                el.classList.add('copy-success');

                // Visual feedback (toast)
                toast.textContent = `Copied ${textToCopy} to clipboard!`;
                toast.classList.add('show');

                // Auditory feedback
                announcer.textContent = `Copied ${textToCopy} to clipboard`;

                bgTimeout = setTimeout(() => {
                    el.classList.remove('copy-success');
                }, 500);

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

            // Visual feedback (toast)
            toast.textContent = 'Failed to copy to clipboard';
            toast.classList.add('copy-error');
            toast.classList.add('show');

            // Auditory feedback
                announcer.textContent = 'Failed to copy to clipboard';

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
