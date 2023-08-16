let cost = document.querySelector("#id_cost");
let profit = document.querySelector("#id_profit_earned");

profit.disabled = true;

if (cost.value < profit.value) {
  alert("Profit can never be less than the cost price");
}
