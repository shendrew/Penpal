import Lottie from "lottie-react";
import { useState, useEffect } from "react";
import animationData from "../../public/assets/animation.json";
import io from 'socket.io-client';

export default function Home() {
  const [data, setData] = useState('');

  useEffect(() => {
    const socket = io(); // connect to websocket server
    socket.on('update', newData => {
      setData(newData)
    })
    return () => {
      socket.disconnect()
    }
  }, []);

  return (
    <>
      <div className="bg-black-200 min-h-screen flex flex-col items-center justify-center h-14 bg-gradient-to-r from-cyan-500 to-blue-500">
        <p className="text-8xl font-bold">Pen Pal</p>
        <Lottie animationData={animationData} />
        <h2 className="text-3xl">Real Time Data</h2>
        <p>{data}</p>
      </div>
    </>
  );
}
