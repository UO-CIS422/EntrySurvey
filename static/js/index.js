/* Skeleton from which dist/main.js is constructed */
import '@polymer/paper-button/paper-button.js';
import '@polymer/paper-slider/paper-slider.js';

function make_slider(element_name) {
      var slider_name = "#slider_" + element_name;
      var label_name = "#label_" + element_name;
      var the_slider = document.querySelector(slider_name);
      console.log("slider name is '" + slider_name + "'");
      console.log("the_slider is " + the_slider);
      var levels_string = the_slider.getAttribute("levels");
      var levels = JSON.parse(levels_string);
      console.log("Slider levels: " + levels);
      the_slider.addEventListener("value-change",
          function() {
            var label=levels[the_slider.value];
            document.querySelector(label_name).textContent =
                the_slider.value + " — " + label;
          }
      );
  }
console.log("index.js (now main.js) loaded")
