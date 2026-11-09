function addPeopleToList() { //Function to add names to the list of people
	const name = document.getElementById('name');
	const email = document.getElementById('email');
	name.style.display = 'block';
	name.style.margin = '0 auto';
	email.style.display = 'block';
	email.style.margin = '0 auto';
	document.getElementById('list').innerHTML += '<div style="display: grid; grid-template-columns: 1fr auto 1fr; align-items: center;">' + 
	'<span style="grid-column: 2; text-align: center;">' + name.value.trim() + '</span>' + 
	'<span style="grid-column: 3; text-align: center;">' + email.value.trim() + '</span>' + 
	'<button2 style="grid-column: 4; justify-self: end;" onclick="removePerson(this)">Remove</button2></div>'; //Add the name to the list
	name.value = ''; // Clear the input fields
	email.value = ''; // Clear the input fields
}

function removePerson(button) { //Function to remove a person from the list
	button.parentElement.remove();
}

function paste(length, people, order) { //The function used in testing to see that all names are there and lined up correctly
	let i = 0;
	while(i<length-1) {
		console.log(order[i] + ': ' + people.get(order[i]) + ' is giving to ' + order[i+1] + ': ' + people.get(order[i+1]));
		i += 1;
	}
	console.log(order[i] + ': ' + people.get(order[i]) + ' is giving to ' + order[0] + ': ' + people.get(order[0]));
}

function process() { //Main function that runs on button press
	const inputString = document.getElementById('list').innerHTML.split('</span>'); //Splits the list of names into an array of strings, each containing a name
	inputString.pop(); //Removes the last element of the array, which is junk due to the split function
	let people = new Map();
	for(let x=0;x<inputString.length;x+=2) {
		people.set(inputString[x].slice(inputString[x].lastIndexOf('>') + 1, inputString[x].length).trim(),
		inputString[x+1].slice(inputString[x+1].lastIndexOf('>') + 1, inputString[x+1].length).trim()); //Slices the string to get just the names, removing the HTML tags
	}
	const names = Array.from(people.keys());
	let order = new Array();

    for(let x=0;x<people.size;x++) { //Actual order randomiser, taking a random person from first list then placing them in a random position in the reordered list
        const randnum1 = Math.floor(Math.random() * names.length);
		order.push(names.splice(randnum1, 1).toString());
	}
  	paste(people.size, people, order);
	email(people.size, people, order);
}

