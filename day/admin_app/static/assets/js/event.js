document.getElementById('project_verticals').addEventListener('change', function () {
      var sigDiv = document.getElementById('sig_div');
      if (this.value === "Special Interest Group (S.I.G)") {
        sigDiv.style.display = "block";  // Show SIG dropdown
      } else {
        sigDiv.style.display = "none";   // Hide SIG dropdown
      }
    });


document.getElementById('project_stakeholder').addEventListener('change', function () {
      var schoolDiv = document.getElementById('school_div');
      if (this.value === "Thalir") {
        schoolDiv.style.display = "block";  // Show SIG dropdown
      } else {
        schoolDiv.style.display = "none";   // Hide SIG dropdown
      }
    });


document.getElementById('project_stakeholder').addEventListener('change', function () {
      var collageDiv = document.getElementById('collage_div');
      if (this.value === "Yuva") {
        collageDiv.style.display = "block";
      } else {
        collageDiv.style.display = "none";
      }
    });


document.getElementById('project_stakeholder').addEventListener('change', function () {
      var associateDiv = document.getElementById('associate_div');
      if (this.value === "Associate Partner") {
        associateDiv.style.display = "block";
      } else {
        associateDiv.style.display = "none";
      }
    });


