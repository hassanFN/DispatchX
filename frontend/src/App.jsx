// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
// import './App.css'

// function App() {
//   const [count, setCount] = useState(0)

//   return (
//     <>
//       <div>
//         <a href="https://vite.dev" target="_blank">
//           <img src={viteLogo} className="logo" alt="Vite logo" />
//         </a>
//         <a href="https://react.dev" target="_blank">
//           <img src={reactLogo} className="logo react" alt="React logo" />
//         </a>
//       </div>
//       <h1>Vite + React</h1>
//       <div className="card">
//         <button onClick={() => setCount((count) => count + 1)}>
//           count is {count}
//         </button>
//         <p>
//           Edit <code>src/App.jsx</code> and save to test HMR
//         </p>
//       </div>
//       <p className="read-the-docs">
//         Click on the Vite and React logos to learn more
//       </p>
//     </>
//   )
// }

// export default App


import React from "react";
import Map from "./components/Map";

const fakeDrivers = [
  { id: "driver1", location: { lat: 40.113, lon: -88.227 }, rating: 4.9, status: "available" },
  { id: "driver2", location: { lat: 40.115, lon: -88.23 }, rating: 4.6, status: "available" },
];

const fakeTasks = [
  { task_id: "task1", pickup: { lat: 40.111, lon: -88.226 } },
  { task_id: "task2", pickup: { lat: 40.112, lon: -88.225 } },
];

function App() {
  return (
    <div style={{ padding: "1rem" }}>
      <h1>DispatchX Map Test</h1>
      <Map drivers={fakeDrivers} tasks={fakeTasks} />
    </div>
  );
}

export default App;

