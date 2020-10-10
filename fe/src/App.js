import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [players, setPlayers] = useState([]);
  const [input, setInput] = useState('');
  const [skip, setSkip] = useState(0)
  const [ammount, setAmmount] = useState(0);

  useEffect(() => {
    // Load initial data from the server on component load
    fetch(`http://${window.location.hostname}:8000/?skip=${skip}`).then(res => {
      if (res.ok) {
        return res.json()
      }
    }).then(res => {
      setPlayers(res)
      setSkip(players.length)
      console.log(players)
    }).catch(err => {
      console.error(err)
    })
  }, [])

  const search = (e) => {
    e.preventDefault()
    fetch(`http://${window.location.hostname}:8000/?q=${input}`).then(res => {
      if (res.ok) {
        return res.json()
      }
    }).then(res => {
      setPlayers(res)
      setAmmount(0);
      setSkip(0);
    }).catch(err => {
      console.error(err)
    })
  }
  
  const loadMore = (e) => {
    // Get the next layer of data
    e.preventDefault()
    fetch(`http://${window.location.hostname}:8000/?skip=${skip}`).then(res => {
      if (res.ok) {
        return res.json()
      }
    }).then(res => {
      setPlayers([...players, ...res])
      setSkip(players.length)
    }).catch(err => {
      console.error(err)
    })
  }

  const getTeam = (e) => {
    // Get the team up to the ammount
    e.preventDefault()

    fetch(`http://${window.location.hostname}:8000`, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        'ammount': ammount
      })
    }).then(res => {
      if (res.ok)
        return res.json()
      alert('Cannot generate team')
    }).then(res => {
      if (res) {
        setSkip(0);
        setPlayers(res)
      }
    }).catch(err => {
      console.log(err);
      alert('An error occured')
    })
  }

  return (
    <div className="container">
      <div className="row">
        <div className="col">
          <input type="text" onChange={(e) => {setInput(e.target.value)}}></input>
          <button onClick={search}>Search</button>
        </div>
        <div className="col">
          <input type="number" value={ammount} onChange={(e) => {setAmmount(e.target.value)}}></input>
          <button onClick={getTeam}>Generate team</button>
          <button onClick={loadMore}>Reset</button>
        </div>
      </div>
      <div className="row">
        <table className="table">
          <thead>
            <tr>
            <th>Photo</th>
            <th>Name</th>
            <th>Age</th>
            <th>Nationality</th>
            <th>Club</th>
            <th>Overall score</th>
            <th>Value</th>
            </tr>
          </thead>
          <tbody>
            { players.map(player => 
              <tr>
                <td><img src={player.photo} alt={player.name}></img></td>
                <td>{player.name}</td>
                <td>{player.age}</td>
                <td>{player.nationality}</td>
                <td>{player.club}</td>
                <td>{player.overall}</td>
                <td>{player.value}</td>
              </tr>)}
          </tbody>
        </table>
      </div>
      <div className="row">
        <button onClick={loadMore}>Load more</button>
      </div>
    </div>
  );
}

export default App;
