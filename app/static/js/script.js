// app/static/js/script.js
function toggleTemplateUpload(selectedValue) {
    const templateUploadGroup = document.getElementById('template_upload_group');
    const pptxFileInput = document.getElementById('pptx_template_file');
    if (selectedValue === 'upload') {
        templateUploadGroup.style.display = 'block';
        pptxFileInput.required = true;
    } else {
        templateUploadGroup.style.display = 'none';
        pptxFileInput.required = false;
    }
}

// Dynamic heading fields for configure_slides.html (if num_slides were changeable there)
// For now, index.html controls num_slides before this page.
// If you want to adjust num_slides on configure_slides.html, you'd add JS like this:
/*
document.addEventListener('DOMContentLoaded', function() {
    const numSlidesInput = document.getElementById('num_slides_configure'); // Assuming an input on configure_slides
    const headingsContainer = document.getElementById('headings_container');
    const initialNumSlides = parseInt(numSlidesInput.value);

    if (numSlidesInput && headingsContainer) {
        numSlidesInput.addEventListener('input', function() {
            const currentNum = parseInt(this.value);
            const existingFields = headingsContainer.children.length;

            if (currentNum > existingFields) {
                for (let i = existingFields + 1; i <= currentNum; i++) {
                    const div = document.createElement('div');
                    div.className = 'form-group slide-heading-group';
                    const label = document.createElement('label');
                    label.htmlFor = 'final_heading_' + i;
                    label.textContent = 'Heading for Slide ' + i + ':';
                    const input = document.createElement('input');
                    input.type = 'text';
                    input.id = 'final_heading_' + i;
                    input.name = 'final_headings';
                    input.required = true;
                    div.appendChild(label);
                    div.appendChild(input);
                    headingsContainer.appendChild(div);
                }
            } else if (currentNum < existingFields) {
                for (let i = existingFields; i > currentNum; i--) {
                    headingsContainer.removeChild(headingsContainer.lastChild);
                }
            }
        });
    }
});
*/

// Ensure the function is called on page load if a template option is pre-selected (e.g. due to form error re-population)
document.addEventListener('DOMContentLoaded', function() {
    const templateChoiceSelect = document.getElementById('template_choice');
    if (templateChoiceSelect) { // Check if the element exists (it's on index.html)
        toggleTemplateUpload(templateChoiceSelect.value);

        // Add AJAX submission logic for pptConfigForm if desired
        const pptConfigForm = document.getElementById('pptConfigForm');
        if(pptConfigForm) {
            pptConfigForm.addEventListener('submit', function(event) {
                // Basic validation for template choice
                if (templateChoiceSelect.value === "") {
                    alert("Please select a template option.");
                    event.preventDefault();
                    return;
                }
                if (templateChoiceSelect.value === "upload") {
                    const fileInput = document.getElementById("pptx_template_file");
                    if (!fileInput.files || fileInput.files.length === 0) {
                        alert("Please upload a PPTX file if you choose the 'Upload' option.");
                        event.preventDefault();
                        return;
                    }
                }
                // Add loading indicator if it's a normal form submission
                const submitButton = this.querySelector('button[type="submit"]');
                if(submitButton) {
                    submitButton.textContent = 'Processing...';
                    submitButton.disabled = true;
                }
            });
        }
    }

    const finalConfigForm = document.getElementById('finalConfigForm');
    if(finalConfigForm) {
        finalConfigForm.addEventListener('submit', function(event) {
            const submitButton = this.querySelector('button[type="submit"]');
            if(submitButton) {
                submitButton.textContent = 'Generating Presentation... Please Wait';
                submitButton.disabled = true;
            }
        });
    }
});