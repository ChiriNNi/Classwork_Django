const domain = 'http://localhost:8000/';

// let list = document.getElementById('list'); 
let list = document.querySelector('#list');
let listLoader = new XMLHttpRequest();

let id = document.querySelector('#id');
let name = document.querySelector('#name');
let rubricLoader = new XMLHttpRequest();

listLoader.addEventListener('readystatechange', () => {
    if (listLoader.readyState == 4) {
        if (listLoader.status == 200) {
            let data = JSON.parse(listLoader.responseText);
            let s = '<ul>', d;
            for (let i = 0; i < data.length; i++) {
                d = data[i];
                s += '<li>' + d.name + ' <a href="' + domain + 
                'api/rubrics/' + d.id + 
                '/" class="detail">Вывести</a></li>';
            }
            s += '</ul>'; 
            list.innerHTML = s; 

            let links = list.querySelector('ul li a.detail'); 
            links.forEach((link) => 
            {link.addEventListener('click', rubricLoad);});
        } else {
            window.alert(listLoader.statusText);
        }
    }
});

rubricLoader.addEventListener('readystatechange', () => {
    if (listLoader.readyState == 4) {
        if (listLoader.status == 200) {
            let data = JSON.parse(rubricLoader.responseText);
            id.value = data.id;
            name.value = data.name; 
        } else {
            window.alert(rubricLoader.statusText);
        }
    }
});

function listLoad() {
    listLoader.open('GET', domain + 'api/rubrics/', true);
    listLoader.send() 
}

function rubricLoad(evt) {
    evt.preventDefault(); 
    rubricLoader.open('GET', evt.target.href, true); 
    rubricLoader.send();
}

listLoad();
