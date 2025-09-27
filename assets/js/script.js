
let checked_nums = 0;

const checkboxs = document.querySelectorAll('input[type="checkbox"]');
if (checkboxs) {
    checkboxs.forEach(checkbox => {
        if (checkbox.checked) {
            checked_nums += 1;
        }
        checkbox.addEventListener("input", function () {
            if (checkbox.checked == true) {
                checked_nums += 1;
                checkbox.checked = true;
            } else {
                checked_nums -= 1;
                checkbox.checked = false;
            }
        });
    });
}

const submit_button = document.getElementById("submit-button");
if (submit_button) {
    submit_button.addEventListener("click", function (event) {
        if (checked_nums <= 0) {
            event.preventDefault();
            alert("يجب ان تختار فئة واحده على الأقل للقسم الواحد");
            return;
        }
    });
}

const carousels = document.getElementsByClassName("carousel-inner");
if (carousels) {
    Array.from(carousels).forEach(carousel => {
        carousel.firstElementChild.className += " active";
    });
}

function productsOrdering() {
    var select = document.getElementById("pord");
    var selectedValue = select.value;
    if (selectedValue != " ") {
        let queryParams = new URLSearchParams(window.location.search)
        queryParams.set("pord", selectedValue);
        window.location.search = queryParams.toString();
    } else {
        let queryParams = new URLSearchParams(window.location.search)
        queryParams.set("pord", "");
        queryParams.delete("pord", "");
        window.location.search = queryParams.toString();
    }
}

function productsPerPage() {
    var select = document.getElementById("ppp");
    var selectedValue = select.value;
    if (selectedValue != " ") {
        let queryParams = new URLSearchParams(window.location.search)
        queryParams.set("ppp", selectedValue);
        window.location.search = queryParams.toString();
    } else {
        let queryParams = new URLSearchParams(window.location.search)
        queryParams.set("ppp", "");
        queryParams.delete("ppp", "");
        window.location.search = queryParams.toString();
    }
}


function visitorsOrdering() {
    var select = document.getElementById("vord");
    var selectedValue = select.value;
    if (selectedValue != " ") {
        let queryParams = new URLSearchParams(window.location.search)
        queryParams.set("vord", selectedValue);
        window.location.search = queryParams.toString();
    } else {
        let queryParams = new URLSearchParams(window.location.search)
        queryParams.set("vord", "");
        queryParams.delete("vord", "");
        window.location.search = queryParams.toString();
    }
}

function visitorsPerPage() {
    var select = document.getElementById("vpp");
    var selectedValue = select.value;
    if (selectedValue != " ") {
        let queryParams = new URLSearchParams(window.location.search)
        queryParams.set("vpp", selectedValue);
        window.location.search = queryParams.toString();
    } else {
        let queryParams = new URLSearchParams(window.location.search)
        queryParams.set("vpp", "");
        queryParams.delete("vpp", "");
        window.location.search = queryParams.toString();
    }
}

page_input = document.getElementById("id_page-number");
if (page_input) {
    page_input.addEventListener("change", function () {
        page_number = page_input.value;
        if (totalPages && parseInt(page_number) && page_number > 0 && page_number <= totalPages) {
            let queryParams = new URLSearchParams(window.location.search)
            queryParams.set("page", page_number);
            window.location.search = queryParams.toString();
        }
        else {
            alert("رقم الصفحة غير صحيح");
        }
    }
    );
}




const regexSpaces = /^\S*$/;
function firstNameValidation() {
    if (firstNameField.value.trim().length >= 3 && firstNameField.value.trim().length < 50) {
        firstNameField.classList.remove("is-invalid");
        firstNameField.classList.add("is-valid");
        return true;
    } else {
        firstNameField.classList.remove("is-valid");
        firstNameField.classList.add("is-invalid");
        return false;
    }
}

function lastNameValidation() {
    if (lastNameField.value.trim().length >= 3 && lastNameField.value.trim().length < 50) {
        lastNameField.classList.remove("is-invalid");
        lastNameField.classList.add("is-valid");
        return true;
    } else {
        lastNameField.classList.remove("is-valid");
        lastNameField.classList.add("is-invalid");
        return false;
    }
}

function emailValidation() {
    const emailRegex = /^([a-zA-Z0-9_\-?]){3,}@([a-zA-Z]){4,}\.([a-zA-Z]){3,5}$/;

    if (regexSpaces.test(emailField.value) && emailRegex.test(emailField.value)) {
        emailField.classList.remove("is-invalid");
        emailField.classList.add("is-valid");
        return true;
    } else {
        emailField.classList.remove("is-valid");
        emailField.classList.add("is-invalid");
        return false;
    }
}

function passwordValidation() {
    if (passwordField.value.trim().length > 0) {
        passwordField.classList.remove("is-invalid");
        passwordField.classList.add("is-valid");
        return true;
    } else {
        passwordField.classList.remove("is-valid");
        passwordField.classList.add("is-invalid");
        return false;
    }
}

function password1Validation() {
    const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*_\-])[A-Za-z\d!@#$%^&*_\-]{10,}$/;
    if (regexSpaces.test(password1Field.value) && passwordRegex.test(password1Field.value)) {
        password1Field.classList.remove("is-invalid");
        password1Field.classList.add("is-valid");
        return true;
    } else {
        password1Field.classList.remove("is-valid");
        password1Field.classList.add("is-invalid");
        return false;
    }
}

function passwordsIdentical() {

    if (password1Validation() && password1Field.value == password2Field.value) {
        password2Field.classList.remove("is-invalid");
        password2Field.classList.add("is-valid");
        return true;
    } else {
        password2Field.classList.remove("is-valid");
        password2Field.classList.add("is-invalid");

        return false;
    }

}

function common1(event) {
    event.preventDefault();
    event.stopPropagation();
    submitButton.classList.remove("btn-primary");
    submitButton.classList.remove("is-valid");
    submitButton.classList.add("is-invalid");
    submitButton.classList.add("btn-danger");
}

function common2(form) {
    submitButton.classList.remove("btn-danger");
    submitButton.classList.remove("btn-primary");
    submitButton.classList.remove("is-invalid");
    submitButton.classList.add("is-valid");
    submitButton.classList.add("btn-outline-success");
    form.classList.add("was-validated");
}

const forms = document.querySelectorAll(".needs-validation");
const firstNameField = document.querySelector("#id_first_name");
const lastNameField = document.querySelector("#id_last_name");
const emailField = document.querySelector("#id_email");
const passwordField = document.querySelector("#id_password");
const password1Field = document.querySelector("#id_password1");
const password2Field = document.querySelector("#id_password2");
const submitButton = document.querySelector("#id_submit");

if (firstNameField && lastNameField && emailField && password1Field && password2Field) {
    // Register New User Page
    firstNameField.addEventListener("blur", firstNameValidation);
    lastNameField.addEventListener("blur", lastNameValidation);
    emailField.addEventListener("blur", emailValidation);
    password1Field.addEventListener("blur", password1Validation);
    password2Field.addEventListener("blur", passwordsIdentical);

    (
        function () {
            if (forms) {
                for (let form of forms) {
                    form.addEventListener(
                        "submit",
                        function (event) {
                            if (
                                !form.checkValidity() ||
                                !firstNameValidation() ||
                                !lastNameValidation() ||
                                !emailValidation() ||
                                !password1Validation() ||
                                !passwordsIdentical()
                            ) {
                                common1(event);
                                firstNameValidation();
                                lastNameValidation();
                                emailValidation();
                                password1Validation();
                                passwordsIdentical();
                            } else {
                                common2();
                                firstNameValidation();
                                lastNameValidation();
                                emailValidation();
                                password1Validation();
                                passwordsIdentical();
                            }
                        }
                    )
                }
            }
        }
    )();
}else if (emailField && passwordField) {
    // login page
    emailField.addEventListener("blur", emailValidation);
    passwordField.addEventListener("blur", passwordValidation);

    (
        function () {
            if (forms) {
                for (let form of forms) {
                    form.addEventListener(
                        "submit",
                        function (event) {
                            if (
                                !form.checkValidity() ||
                                !emailValidation() ||
                                !passwordValidation()
                            ) {
                                common1(event);
                                emailValidation();
                                passwordValidation();
                            } else {
                                common2(form);
                                emailValidation();
                                passwordValidation();
                            }
                        }
                    )
                }
            }
        }
    )();
}

productForm = document.getElementById('product-form');
if (productForm) {        
    productForm.onsubmit = function(e) {
        var inputFiles = document.getElementById('files');
        var maxSizeMB = 2;  // Maximum file size in MB
        var maxSizeBytes = maxSizeMB * 1024 * 1024;

        if (inputFiles.files.length > 0 && inputFiles.files.length <= 4) {
            for (const file of inputFiles.files) {
                var fileSize = file.size; 
                var fileType = file.type; 
                if (fileSize > maxSizeBytes) {
                    e.preventDefault();  // Prevent form submission
                    alert("يجب ان يكون حجم الملف الواحد اقل من 2 ميجابايت");
                    return ;
                }else if (fileType != "image/jpeg" && fileType != "image/jpg" && fileType != "image/png" && fileType != "video/mp4") {
                    e.preventDefault();  // Prevent form submission
                    alert("يجب ان تختار صورة من نوع jpg, jpeg, png او فيديو من نوع mp4");
                    return;
                }
            }
        }else {
            e.preventDefault();  // Prevent form submission
            alert("يجب ان يكون للمنتج ملف واحد على الاقل واربعة ملفات كحد اقصى");
        }
    };
}


departmentForm = document.getElementById('department-form');
if (departmentForm) {
    departmentForm.onsubmit = function (e) {
        var inputImage = document.getElementById('id_image');
        var maxSizeMB = 2;  // Maximum file size in MB
        var maxSizeBytes = maxSizeMB * 1024 * 1024;
        if (inputImage.files.length > 0) {
            var fileSize = inputImage.files[0].size;
            var fileType = inputImage.files[0].type;
            if (fileSize > maxSizeBytes) {
                e.preventDefault();  // Prevent form submission
                alert("يجب ان يكون حجم الملف الواحد اقل من 2 ميجابايت");
                return;
            } 
            else if (fileType != "image/jpeg" && fileType != "image/jpg" && fileType != "image/png") {
                e.preventDefault();  // Prevent form submission
                alert("يجب ان تختار صورة");
                return;
            }
        }
    };
}