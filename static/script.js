const display = document.getElementById("display");
const buttons = document.querySelectorAll("#buttons button");
const form = document.querySelector("form");

let current = "";

buttons.forEach(button => {
  button.addEventListener("click", () => {
    const value = button.textContent;

    if (value === "AC") {
      current = "";
      display.value = "0";
    } else if (value === "=") {
      
      form.submit();
    } else {
      current += value;
      display.value = current;
    }
  });
});
