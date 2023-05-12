// for ReactJS usage
// import { createRoot } from 'react-dom/client';

// const mediaRecorder = new MediaRecorder(stream);
const recordBtn = document.getElementById('audioInput');
const recordBtnText = recordBtn.firstElementChild;
const recordedAudioContainer = document.getElementById('recordedAudioContainer');
const queryInputText = document.getElementById('qTextInput');
const getResponsebtn = document.getElementById('getReponseBtn');

let chunks = []; //will be used later to record audio
let mediaRecorder = null; //will be used later to record audio
let audioBlob = null; //the blob that will hold the recorded audio

// display state values for the record button
const recordBtnRecordingView = `
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-mic-mute-fill text-danger" viewBox="0 0 16 16">
    < path d = "M13 8c0 .564-.094 1.107-.266 1.613l-.814-.814A4.02 4.02 0 0 0 12 8V7a.5.5 0 0 1 1 0v1zm-5 4c.818 0 1.578-.245 2.212-.667l.718.719a4.973 4.973 0 0 1-2.43.923V15h3a.5.5 0 0 1 0 1h-7a.5.5 0 0 1 0-1h3v-2.025A5 5 0 0 1 3 8V7a.5.5 0 0 1 1 0v1a4 4 0 0 0 4 4zm3-9v4.879L5.158 2.037A3.001 3.001 0 0 1 11 3z" />
    <path d="M9.486 10.607 5 6.12V8a3 3 0 0 0 4.486 2.607zm-7.84-9.253 12 12 .708-.708-12-12-.708.708z" /> 
</svg > `;  //Stop Recording

const recordBtnStopView = `
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-mic-fill text-danger" viewBox = "0 0 16 16" >
    <path d="M5 3a3 3 0 0 1 6 0v5a3 3 0 0 1-6 0V3z" />
    <path d="M3.5 6.5A.5.5 0 0 1 4 7v1a4 4 0 0 0 8 0V7a.5.5 0 0 1 1 0v1a5 5 0 0 1-4.5 4.975V15h3a.5.5 0 0 1 0 1h-7a.5.5 0 0 1 0-1h3v-2.025A5 5 0 0 1 3 8V7a.5.5 0 0 1 .5-.5z" /> 
</svg >`; //Record Prompt

//----------------------------------------------------------------------
// App component
//----------------------------------------------------------------------
// export default function kaito(){
  
// }

// function kaitoFormElem(params) {
//   return(
    
//   )
// }

// function getReponseButton({onClick}) {
//   return(
//     <button onClick={onClick} className="btn btn-dark btn-lg rounded-pill" id="getReponseBtn">
//       Get Response
//     </button>
//   );
// }
// const domBtnNode = document.getElementById('getResponseDiv');
// const root = createRoot(domBtnNode);
// root.render(<getReponseButton onClick={processInputPrompt}/>);

// function Button({ onClick, children }) {
//   return (
//     <button onClick={onClick}>
//       {children}
//     </button>
//   );
// }

//------------------------------------------------------------------------
// media functions
//------------------------------------------------------------------------
function record(){
    //check if browser supports getUserMedia
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert('Your browser does not support recording!');
        return;
    }

    //recordBtnText.innerHTML = recordBtnText.innerHTML.includes('Record Prompt') ? recordBtnRecordingView : recordBtnStopView;
    recordBtnText.innerHTML = mediaRecorder && mediaRecorder.state === 'recording' ? recordBtnStopView : recordBtnRecordingView ;

    if (!mediaRecorder) {
        // start recording
        navigator.mediaDevices.getUserMedia({

            audio: true,

        }).then((stream) => {

            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();
            mediaRecorder.ondataavailable = mediaRecorderDataAvailable;
            mediaRecorder.onstop = mediaRecorderStop;

        }).catch((err) => {

            alert(`The following error occurred: ${err}`);
            // change image in button
            recordBtnText.innerHTML = recordBtnStopView;

        });
    } else {
        // stop recording
        mediaRecorder.stop();
    }

}

recordBtn.addEventListener('click', record);


function mediaRecorderDataAvailable(e) {
    chunks.push(e.data);
}


function mediaRecorderStop() {
    //check if there are any previous recordings and remove them
    // if (recordedAudioContainer.firstElementChild.tagName === 'AUDIO') {
    //     recordedAudioContainer.firstElementChild.remove();
    // }
    if (recordedAudioContainer.firstElementChild != null) {
        recordedAudioContainer.firstElementChild.remove();
    }
    //create a new audio element that will hold the recorded audio
    const promptAudioElem = document.createElement('audio');
    promptAudioElem.setAttribute('controls', ''); //add controls
    promptAudioElem.setAttribute('id', 'recordedAudioPrompt');
  
    //create the Blob from the chunks
    audioBlob = new Blob(chunks, { type: 'audio/mp3' });
    const audioURL = window.URL.createObjectURL(audioBlob);
    promptAudioElem.src = audioURL;

    // if audio recorded, disable text input
    if (audioBlob != null){
        queryInputText.setAttribute('readonly','')
    }
    

    //show audio
    // recordedAudioContainer.insertBefore(promptAudioElem, recordedAudioContainer.firstElementChild);
    recordedAudioContainer.appendChild(promptAudioElem);
    recordedAudioContainer.classList.add('d-flex');
    recordedAudioContainer.classList.remove('d-none');

    const discardButton = document.createElement("button");
    discardButton.setAttribute('class', 'btn btn-danger rounded-pill'); 
    discardButton.setAttribute('id', 'discardButton'); 
    discardButton.setAttribute('data-bs-toggle', 'tooltip')
    discardButton.setAttribute('data-bs-placement', 'top')
    discardButton.setAttribute('data-bs-title', 'Delete recorded audio.')
    discardButton.setAttribute('style', 'z-index: 100;')
    // discardButton.innerHTML = "Discard";
    discardButton.innerHTML = `
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3-fill" viewBox="0 0 16 16">
     <path d="M11 1.5v1h3.5a.5.5 0 0 1 0 1h-.538l-.853 10.66A2 2 0 0 1 11.115 16h-6.23a2 2 0 0 1-1.994-1.84L2.038 3.5H1.5a.5.5 0 0 1 0-1H5v-1A1.5 1.5 0 0 1 6.5 0h3A1.5 1.5 0 0 1 11 1.5Zm-5 0v1h4v-1a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5ZM4.5 5.029l.5 8.5a.5.5 0 1 0 .998-.06l-.5-8.5a.5.5 0 1 0-.998.06Zm6.53-.528a.5.5 0 0 0-.528.47l-.5 8.5a.5.5 0 0 0 .998.058l.5-8.5a.5.5 0 0 0-.47-.528ZM8 4.5a.5.5 0 0 0-.5.5v8.5a.5.5 0 0 0 1 0V5a.5.5 0 0 0-.5-.5Z"/>
    </svg>`
    recordedAudioContainer.appendChild(discardButton);
  
    // handle discard button click
    discardButton.addEventListener('click', discardRecording)

    //hide record button
    recordBtn.classList.add('d-none')

    // completed recording action
    // promptAudioElem.addEventListener('complete', () => {
    //     getResponsebtn.click();
    // });
    // place tab focus on get response button.
    // getResponsebtn.setAttribute('tabindex', '-1');

    //reset to default
    mediaRecorder = null;
    chunks = [];
}


function discardRecording() {
  if (recordedAudioContainer.firstElementChild != null) {
      //remove the audio tag for recorded audio playback
      recordedAudioContainer.firstElementChild.remove();
      //hide recordedAudioContainer
      recordedAudioContainer.classList.add('d-none');
      recordedAudioContainer.classList.remove('d-flex');
  }
  //reset audioBlob for the next recording
  audioBlob = null;

  // display record button
  recordBtn.classList.remove('d-none')

  // activate query text input 
  queryInputText.removeAttribute('readonly')
};

//----------------------------------------------------------------------
// input query processing functions
//----------------------------------------------------------------------
async function postPromptData(data) {
  const response = await fetch("/resources/kaito/prompt_processor", {
    method: "POST",
    body: data,
  })

  if (!response.ok) {
    throw new Error(`Request failed with status ${reponse.status}`)
  }

  // getResponsebtn.innerHTML = `Get Response`;
  getResponsebtn.innerHTML = `
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-send-fill" viewBox="0 0 16 16">
    <path d="M15.964.686a.5.5 0 0 0-.65-.65L.767 5.855H.766l-.452.18a.5.5 0 0 0-.082.887l.41.26.001.002 4.995 3.178 3.178 4.995.002.002.26.41a.5.5 0 0 0 .886-.083l6-15Zm-1.833 1.89L6.637 10.07l-.215-.338a.5.5 0 0 0-.154-.154l-.338-.215 7.494-7.494 1.178-.471-.47 1.178Z"/>
  </svg>`;
  
  getResponsebtn.removeAttribute('disabled','');
  window.location.reload(true) // reload page to reflect new data
  return response;
}


function processInputPrompt(){
  //form data to hold the Blob to send in user HTML request
  const formData = new FormData();

  //add the audio blob or query text to formData
  if (audioBlob != null){
      formData.append('audio', audioBlob, 'voice_prompt.mp3');
  } else {
      if (queryInputText.value != null){
          formData.append('text', queryInputText.value);
      }  
  }

  // for debug purpose. comment in production deployment
  // console.log(formData.has('audio') || formData.get('text').length != 0); 

  // send POST request if user input is provided
  if (formData.has('audio') || formData.get('text').length != 0){
      // disable button and indicate processing 
      getResponsebtn.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>`; //Processing...
      getResponsebtn.setAttribute('disabled','');

      // send request
      //const request = new XMLHttpRequest();
      //request.open('POST', '/resources/kai/query_processor');
      //request.send(formData);
      const response = postPromptData(formData);
      //console.log(response);
  }
    
}

// response button click action
getResponsebtn.addEventListener('click', processInputPrompt);

// Return key press action
queryInputText.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        getResponsebtn.click();
    }
});