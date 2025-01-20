function toggleSigOption() {
    var projectVertical = document.getElementById('project_verticals').value;  // Fixing variable name to match the correct ID
    var sigOption = document.getElementById('sig_options');  // Corrected the variable name

    if (projectVertical === 'Special Interest Group (S.I.G)') {  // Fixed the syntax of the if condition
        sigOption.style.display = 'block';  // Show the SIG options
    } else {
        sigOption.style.display = 'none';  // Hide the SIG options if the condition is not met
    }
}
