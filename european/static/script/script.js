// Clear storage
window.localStorage.clear();

// Autocomplete function from typehead.js library
let substringMatcher = function(strs) {
    return function findMatches(q, cb) {
      var matches, substringRegex;
      matches = [];
      substrRegex = new RegExp(q, 'i');
      $.each(strs, function(i, str) {
        if (substrRegex.test(str)) {
          matches.push(str);
        }
      });
      cb(matches);
    };
  };

  // Array to iterate through
  let euCountries = ["Albania", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Czechia", "Denmark", "Estonia", "Finland", "France", "Germany","Greece", "Hungary", "Iceland", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "North Macedonia", "Moldova, Republic of", "Montenegro", "Netherlands", "Norway", "Poland", "Portugal", "Romania", "Russian Federation", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Turkey", "Ukraine", "United Kingdom"];
  
  $('#the-basics .typeahead').typeahead({
    hint: true,
    highlight: true,
    minLength: 1
  },
  {
    name: 'euCountries',
    source: substringMatcher(euCountries)
});

// Get countries from flask app
function getData(data){
  document.getElementById("visited").innerText = data.length;
  document.getElementById("max").innerText = euCountries.length;
  return data
}

// Show overlay
function overlayOn(){
  document.getElementById("overlay").style.display = "flex";
  $(".typeahead").focus();
}

// Hide overlay
function overlayOff(){
  document.getElementById("overlay").style.display = "none";
}

// Call check country every time key is pressed or something is clicked
document.getElementById("overlay").addEventListener("keyup", checkCountry);
document.getElementById("overlay").addEventListener("click", checkCountry);

// Check for remove country every time map is clicked
document.getElementById("map").addEventListener("click", checkForRemove);

// Check country name and enable plus button
function checkCountry(){
  let inp = document.getElementById("countryname");
  let btn = document.getElementById("add-btn");
  if(euCountries.includes(inp.value)){
    btn.disabled = false;
    btn.style.backgroundColor = "var(--blue)";
  }
  else{
    btn.disabled = true;
    btn.style.backgroundColor = "rgba(255,255,255,0.5)";
  }
}

// Check if visited country is clicked and ask for remove
function checkForRemove(e){
  if(e.path[0].getAttribute("data-info")){
    if(e.target.classList[1]){
      if(e.target.classList[1].length == 3){
        let countryCode = e.target.classList[1];
        let countries = {
          "countryCode": countryCode
        }
        $.confirm({
          title: 'Delete?',
          content: 'You will remove country from list.',
          buttons: {
              confirm: function () {
                $.ajax({
                  url: Flask.url_for('my_function'),
                  type: 'POST',
                  data: JSON.stringify(countries), 
                  })
                  .done(function(result){
                    $.alert(result);
                    window.location.href = "/";
                  })
              },
              cancel: function () {
              }
          }
        });




      }
    }
  } 
}