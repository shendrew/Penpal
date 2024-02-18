import Lottie from "lottie-react";
import { useState, useEffect } from "react";
import animationData from "../../public/assets/animation.json";
import io from "socket.io-client";

export default function Home() {
  const [ml_data, mlSetData] = useState("");
  const [data, setData] = useState("");
  useEffect(() => {
    const socket = io("http://localhost:5000"); // connect to websocket server
    socket.on("update", (data) => {
      // receives data
      // mlSetData(ml_data)
      setData(data.displacement);
      console.log("data is", data);
    });
    return () => {
      socket.disconnect();
    };
  }, []);

  return (
    <>
      <div className="font-sans	bg-black-200 flex flex-col items-center justify-center bg-gradient-to-r from-cyan-500 to-blue-500">
        <p className="text-8xl font-bold text-emerald-100	pb-24 pt-10">Pen Pal</p>
        <Lottie animationData={animationData} />
        <p className="text-5xl text-emerald-100 pt-28 pb-5">EMNIST Examples</p>
        <img src="/assets/EMNIST.jpg" width={800} />
        <h2 className="text-5xl text-emerald-100 pt-20">Real Time Data</h2>
        <div className="flex space-x-80 pt-20 pb-20">
          <p>child1</p>
          <p>chil2</p>
        </div>
        {/* <p>ML data: {ml_data}</p> */}
        <p className="text-5xl text-emerald-100">Measurements: {data}</p>
        <div className="flex justify-between">
          <p>asdasds</p>
          <p>popinfoew</p>
        </div>
      </div>
    </>
  );
}
