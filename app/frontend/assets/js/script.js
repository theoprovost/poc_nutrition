// Video related
const videoBox = document.querySelector('#video_box')
const btn_ocam = document.querySelector('#btn_ocam')

if (btn_ocam !== null) {
    btn_ocam.addEventListener('click', _ => initVideo())
    originalTxt = btn_ocam.textContent
}

// Content related
const resBox = document.querySelector('#res_box')

const charts_btn = document.querySelector('#charts_btn')
const return_btn = document.querySelector('#return_btn')
const return_btn_index_chart = document.querySelector('#return_btn_index_chart')
const quit_btn = document.querySelector('#quit_btn')


if (charts_btn !== null) {
    charts_btn.addEventListener('click', _ => location.href = '/charts')
}
if (return_btn !== null) {
    return_btn.addEventListener('click', _ => location.href = '/')
}
if (return_btn_index_chart !== null) {
    return_btn_index_chart.addEventListener('click', _ => {
        location.href = '/charts'
    })
}
if (quit_btn !== null) {
    quit_btn.addEventListener('click', _ => {
        console.log('click')
        info_box.style.height = '0'
        info_box.style.width = '0'
        info_box.style.padding = '0'
    })
}


function createVideoElAndSurrounding() {
    if (typeof video !== 'undefined') {
        resBox.innerHTML = ''
        videoBox.innerHTML = ''
        btn_ocam.textContent = originalTxt
    }

    video = document.createElement('video')
    video.setAttribute('width', 640)
    video.setAttribute('height', 480)
    video.setAttribute('AutoPlay', true)
    video.classList = 'box'
    videoBox.appendChild(video)

    if (typeof variable !== 'undefined') {
        btnVal.textContent = originalTxt
    }

    return video
}


async function processCode(code) {
    btn_ocam.textContent = `Searching EAN-13 :  ${code} 🔍`
    await fetch(`https://poc-nutrition.herokuapp.com/api/search/${code}`, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            "X-Requested-With": "XMLHttpRequest"
        }
    }).then(res => {
        return res.json()
    }).then(res => {
        if (res.code == 200) {
            printResults(res.data)
        } else {
            let p = document.createElement('p')
            p.textContent = res.message
            p.classList = 'tag is-danger is-light'
            resBox.appendChild(p)

            let btnVal = document.createElement('button')
            btnVal.id = 'validation'
            btnVal.textContent = 'OK'
            btnVal.classList = 'tag is-danger is-light'
            btnVal.style.border = '1px solid #ccc'

            btnVal.addEventListener('click', _ => initVideo())
            resBox.appendChild(btnVal)
        }
    })
}

function initVideo() {
    video = createVideoElAndSurrounding()

    if (video && navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        const constraints = {
            video: true,
            audio: false
        }

        navigator.mediaDevices.getUserMedia(constraints).then(stream => video.srcObject = stream);

        const detector = new BarcodeDetector({ formats: ['ean_13'] })
        const detectCode = () => {
            detector.detect(video)
                .then(codes => {
                    if (codes.length === 0) return; // If not scanned return
                    if (codes.length > 0) {
                        clearVideo()
                        code = codes[0].rawValue
                        processCode(code)
                    }
                }).catch(err => {
                    console.log(err);
                })
        }

        int = setInterval(detectCode, 100)
    }
}

function clearVideo() {
    clearInterval(int)
    video.pause()
    video = false
}

function printResults(data) {
    function createTable(data) {
        const table_box = document.querySelector('#table_box > table > tbody')

        for (const prop in data) {
            let x = table_box.insertRow()
            let y = x.insertCell()
            let z = document.createTextNode(prop)
            y.appendChild(z)

            let a = x.insertCell()
            let b = document.createTextNode(data[prop])
            a.appendChild(b)
        }
    }
    //createTable(data)

    results = {
        'fat': data['fat_100g'],
        'sugars': data['sugars_100g'],
        'saturated_fat': data['saturated-fat_100g'],
        'carbs': data['carbohydrates_100g'],
        'proteins': data['proteins_100g'],
        'salt': data['salt_100g'],
        'energy': data['energy-kcal_100g']
    }

    threshold = 5

    function createResultDisplay(data) {
        info_box.style.height = '100vh'
        info_box.style.width = '80vw'
        info_box.style.padding = '120px !important'

        let css_class
        exclude = ['energy']
        for (const [k, v] of Object.entries(data)) {
            if (exclude.includes(k)) return

            if (v > threshold) {
                css_class = 'res-red';
            } else css_class = 'res-green'

            info_box.innerHTML += `<div class="box rm-borders">
                                        <img src="./icons/${k}.svg" alt="${k}" class="${css_class}">
                                        <p class='${css_class}'>${v}</p>
                                    </div>`
        }

    }
    createResultDisplay(results)
}
