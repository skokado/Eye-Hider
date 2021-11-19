import { useState, useEffect, useRef } from 'react';

import Header from './components/Header'
import Button from './components/Button'

function App() {
  const [isInitial, setIsInitial] = useState(true)
  const [canHideEyes, setCanHideEyes] = useState(false)
  const [canDownload, setCanDownload] = useState(false)
  const [errorMessage, setErrorMessage] = useState("")

  const video = useRef(null)
  const videoConstraints = {
    audio: false,
    video: {
      width: 720,
      height: 480
    }
  }
  const canvas = useRef(null)
  const img = useRef(null)

  const takeSnapshot = () => {
    setCanDownload(false)
    canvas.current.width = video.current.videoWidth
    canvas.current.height = video.current.videoHeight
    const ctx = canvas.current.getContext("2d")
    ctx.drawImage(
      video.current, 0, 0,
      canvas.current.width,
      canvas.current.height
    )
    canvas.current.toBlob(async (blob) =>{
      img.current.src = URL.createObjectURL(blob)
    })
    setIsInitial(false)
    setCanHideEyes(true)
  }

  const hideEyes = async () => {
    const apiBaseUrl = process.env.API_HOST || "http://localhost:8000"
    
    canvas.current.toBlob(async (blob) => {
      try {
        const response = await fetch(
          `${apiBaseUrl}/hide-eyes`, {
            method: "POST",
            body: blob,
          }
        )
        // Image を生成
        if (response.status === 200 ) {
          const data = await response.blob()
          img.current.src = URL.createObjectURL(data)
          setCanDownload(true)
        } else {
          setErrorMessage("顔が検出されませんでした")
          setIsInitial(true)
          setCanDownload(false)
        }
        setCanHideEyes(false)
      } catch (e) {
        console.log(e)
        setErrorMessage("リクエストエラーが発生しました")
        setIsInitial(true)
        setCanHideEyes(false)
        setCanDownload(false)
      }
    })
  }
  
  // Get Video
  useEffect(() => {
    (async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia(videoConstraints)
        video.current.srcObject = stream
        video.current.play()
      } catch (e) {
        console.log(e)
      }
    })();
  })

  return (
    <>
    <Header />
    <div className="container">
      <div className="columns is-vcentered">
        <div className="column is-half">
          {/* Webカメラの映像 */}
          <video id="video" ref={video}></video>
        </div>
        <div className="column is-half has-text-centered">
          {/* スナップショット/目線画像 */}
          {(() => {
            if (canHideEyes) {
              return (<>
                <canvas ref={canvas} style={{display: "none"}}></canvas>
                <img alt="" ref={img}></img>
              </>)
            } else {
              if (isInitial) {
                return (<>
                  <canvas ref={canvas} style={{display: "none"}}></canvas>
                  <img alt="" ref={img} style={{display: "none"}}></img>
                  <p>{!(!errorMessage) ? errorMessage : "Webカメラのキャプチャがここに表示されます"}</p>
                </>)
              } else {
                return (<>
                  <canvas ref={canvas} style={{display: "none"}}></canvas>
                  <img alt="" ref={img}></img>
                </>)
              }
            }
          })()}
        </div>
      </div>
      <div className="columns">
        <div className="column is-half has-text-centered">
          <Button
            buttonClass="is-primary"
            text="スナップショットを撮る"
            onClick={takeSnapshot}
          />
        </div>
        <div className="column is-half has-text-centered">
          <div className="columns">
            <div className="column">
              <Button
                buttonClass="is-primary"
                text="目線をつける"
                disabled={!canHideEyes}
                onClick={hideEyes}
              />
            </div>
            <div className="column">
              { canDownload ? <a href={img.current.src} className="button is-info" download="mask.png">ダウンロード</a>
               : <Button buttonClass="is-info" disabled="disabled" text="ダウンロード"/>}
            </div>
          </div>
        </div>
      </div>
    </div>
    </>
  );
}

export default App;
