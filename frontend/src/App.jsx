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
import useDrivers from "./hooks/useDrivers";
import useTasks from "./hooks/useTasks";

function App() {
  const { drivers, loading: loadingDrivers } = useDrivers();
  const { tasks, loading: loadingTasks } = useTasks();

  if (loadingDrivers || loadingTasks) {
    return <div>Loading...</div>;
  }

  return (
    <div style={{ padding: "1rem" }}>
      <h1>DispatchX Map</h1>
      <Map drivers={drivers} tasks={tasks} />
    </div>
  );
}

export default App;

