import Lottie from "lottie-react";
import { useState, useEffect } from "react";
import animationData from "../../public/assets/animation.json";
import io from "socket.io-client";

export default function Home() {
  // const [letterData, setLetterData] = useState("");
  const [dispData, setDispData] = useState("");
  useEffect(() => {
    const socket = io("http://localhost:5000"); // connect to websocket server
    socket.on("update", (data) => {
      console.log("data is ", data)
      setDispData(data.displacement)
      // setDispData(data.displacement);
    });
    return () => {
      socket.disconnect();
    };
  }, []);

  return (
    <>
      <div className="font-sans	bg-black-200 flex flex-col items-center justify-center bg-gradient-to-r from-cyan-500 to-blue-500">
        <p className="text-8xl font-bold text-emerald-100	pb-24 pt-10">
          Pen Pal
        </p>
        <Lottie animationData={animationData} />
        <p className="text-5xl text-emerald-100 pt-28 pb-5">
          The Alphabet and EMNIST
        </p>
        <img src="/assets/EMNIST.jpg" width={800} />
        <div className="flex flex-col">
        <div className="flex justify-center align-center space-x-20">
          <h2 className="text-5xl text-emerald-100 pt-20">Displacement</h2>
          <p className="text-5xl text-emerald-100">{dispData}</p>
        </div>
        <div className="flex justify-center align-center space-x-20">
          <h2 className="text-5xl text-emerald-100 pt-20">Letter Guessed</h2>
          {/* <p className="text-5xl text-emerald-100">{letterData}</p> */}
        </div>
        </div>
        <div className="flex space-x-80 pt-20 pb-20"></div>
        {/* <p>ML data: {ml_data}</p> */}
        <p className="text-5xl text-emerald-100">Drawing Board</p>
        <div className="flex justify-between">
          <p>asdasds</p>
          <p>popinfoew</p>
        </div>
      </div>
    </>
  );
}
