import { Product, addProductToTable } from './data.js';

let formWindow = document.getElementById('modalForm');
let form = document.getElementById('formAdd');
let commodityAddBtn = document.getElementById('btnAdd');
let saveButton = document.getElementById('btnSave');
let closeButton = document.getElementById('btnClose');
// const productTable = document.getElementById('productTable');

commodityAddBtn.addEventListener('click', () => {
	formWindow.classList.remove('hidden');
	document.body.classList.add('overflow-hidden');
	console.log('Modal opened');
});

closeButton.addEventListener('click', () => {
	formWindow.classList.add('hidden');
	document.body.classList.remove('overflow-hidden');
	console.log('Modal closed');
});

// Walidation

form.addEventListener('submit', event => {
	event.preventDefault();
	let name = document.getElementById('name').value;
	let amount = document.getElementById('amount').value;
	let minAmount = document.getElementById('minAmount').value;
	let category = document.getElementById('category').value;
	let localization = document.getElementById('localization').value;
	let errorMessage = '';

	let labels = [name, amount, minAmount, category, localization];

	labels.forEach((label, index) => {
		if (!label) {
			errorMessage += `Pole ${index + 1} jest wymagane.\n`;
		}
	});

	if (errorMessage) {
		alert(errorMessage);
		return;
	}

	console.log('Wszystskie pola są wypełnione ');

	const item1 = new Product(name, amount, minAmount, category, localization);
	addProductToTable(item1);
	form.reset();
	formWindow.classList.add('hidden');
	document.body.classList.remove('overflow-hidden');
	console.log('Produkt dodany do tabeli');

	alert('Towar został dodany pomyślnie!');
});
