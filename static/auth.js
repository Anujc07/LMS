
const auth = (id, value) =>{
    const error = document.getElementById('error');
    const addBtn = document.getElementById('addBtn');
    const regex = /[^a-z A-Z.]/
    valid = regex.test(value);
    if (valid) {        
        if (id === 'username'){
            document.getElementById('uerror').style.display = 'block';
            document.getElementById('addBtn').disabled = true;
        }
        else{
            error.style.display = 'block';       
            document.getElementById('addBtn').disabled = true;
        }
            
    }
    else{
        error.style.display = 'none'; 
        document.getElementById('addBtn').disabled = false;    
        document.getElementById('uerror').style.display = 'none';  
    }

}




function togglePassword() {
    var passwordInput = document.getElementById('password-input');
    var passwordAddon = document.getElementById('password-addon');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        passwordAddon.innerHTML = '<i class="ri-eye-off-fill align-middle"></i>';
    } else {
        passwordInput.type = 'password';
        passwordAddon.innerHTML = '<i class="ri-eye-fill align-middle"></i>'
    }
}