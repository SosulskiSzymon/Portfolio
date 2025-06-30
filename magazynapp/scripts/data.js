// import {
// 	formWindow,
// 	form,
// 	commodityAddBtn,
// 	saveButton,
// 	closeButton,
// } from './formscript.js';

const productTable = document.getElementById('productTable');

class Product {
	constructor(name, amount, minAmount, category, localization) {
		this.name = name;
		this.amount = amount;
		this.minAmount = minAmount;
		this.category = category;
		this.localization = localization;
	}
}

const addProductToTable = product => {
	const row = productTable.insertRow();
	row.insertCell(0).innerText = product.name;
	row.insertCell(1).innerText = product.amount;
	row.insertCell(2).innerText = product.minAmount;
	row.insertCell(3).innerText = product.category;
	row.insertCell(4).innerText = product.localization;
};

export { Product, addProductToTable };
