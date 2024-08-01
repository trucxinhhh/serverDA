import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    const interval = setInterval(() => {
      // Fetch data from API every 1 second
      axios.get('http://192.168.1.199:8000/data/all')
        .then(response => {
          const responseData = response.data;
          console.log(responseData);
          if (responseData && responseData.data) {
            setData(responseData.data);
          }
        })
        .catch(error => console.error('Error fetching data:', error));
    }, 1000);

    return () => clearInterval(interval); // Clear the interval on component unmount
  }, []);

  return (
    <div className="App">
      <h1>Sensor Data</h1>
      {data.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>CO2</th>
              <th>Temperature</th>
              <th>Humidity</th>
              <th>EC</th>
              <th>Pressure</th>
              <th>Flowmeters</th>
              <th>pH</th>
              <th>Water Level 1</th>
              <th>Water Level 2</th>
              <th>Motor 1</th>
              <th>Motor 2</th>
              <th>Motor 3</th>
            </tr>
          </thead>
          <tbody>
            {data.map((item) => (
              <tr key={item.id}>
                <td>{item.id}</td>
                <td>{item.CO2}</td>
                <td>{item.Temp}</td>
                <td>{item.Humi}</td>
                <td>{item.EC}</td>
                <td>{item.Pressure}</td>
                <td>{item.Flowmeters}</td>
                <td>{item.pH}</td>
                <td>{item.WaterlevelSensor1}</td>
                <td>{item.WaterlevelSensor2}</td>
                <td>{item.motor1}</td>
                <td>{item.motor2}</td>
                <td>{item.motor3}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No data available</p>
      )}
    </div>
  );
}

export default App;
