import sqlite3
from contextlib import closing
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(title="Industrial Sensor Platform")

DB_PATH = Path(__file__).with_name("sensors.db")

def connect_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with closing(connect_db()) as db:
        db.execute("""
                   CREATE TABLE IF NOT EXISTS sensors (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL UNIQUE,
                       temperature REAL NOT NULL,
                       status TEXT NOT NULL
                   )
                   """)
        

init_db()


class SensorInput(BaseModel):
    name:str = Field(min_length=1, max_length=80)
    temperature: float = Field(ge=-50, le=250)
    status: str = Field(pattern="^(online|offline)$")
    

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/sensors", status_code=201)
def create_sensor(sensor: SensorInput):
    try:
        with closing(connect_db()) as db:
            cursor = db.execute(
                """
                INSERT INTO sensors (name, temperature, status)
                VALUES (?, ?, ?)
                """,
                (sensor.name, sensor.temperature, sensor.status)
            )
            db.commit()
            sensor_id = cursor.lastrowid
        
        return {"id": sensor_id, **sensor.model_dump()}
    
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409, detail="Sensor name already exsists"
        )
        
        
@app.get("/api/sensors")
def list_sensors():
    with closing(connect_db()) as db:
        rows = db.execute(
            "SELECT * FROM sensors ORDER BY id"
        ).fetchall()
    
    return [dict(row) for row in rows]


@app.get("/api/sensors/{sensor_id}")
def get_sensor(sensor_id: int):
    with closing(connect_db()) as db:
        row = db.execute(
            "SELECT * FROM sensors WHERE id = ?",
            (sensor_id,),
        ).fetchone()
        
    if row is None:
        raise HTTPException(status_code=404, detail="Senosr not found")
    
    return dict(row)


@app.patch("/api/sensors/{sensor_id}")
def update_sensor(sensor_id: int, sensor: SensorInput):
    with closing(connect_db()) as db:
        cursor = db.execute(
            """ UPDATE sensors
            SET name = ?, temperature = ?, status= ?
            WHERE id = ?
            """,
            (
                sensor.name,
                sensor.temperature,
                sensor.status,
                sensor_id
            ),
        )
        db.commit()
        
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Senosr not found")
    
    return {"id": sensor_id, **sensor.model_dump()}


@app.delete("/api/sensors/{sensor_id}", status_code=204)
def delete_sensor(sensor_id:int):
    with closing(connect_db()) as db:
        cursor = db.execute(
            "DELETE FROM sensors WHERE id = ?", (sensor_id,),
        )
        db.commit()
    
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Senosr not found")
    
    return {"message": "Sensor deleted successfully"}
    
    
@app.get("/", response_class=HTMLResponse)
def dashboard():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Industrial Sensor Dashboard</title>
    </head>
    <body>
      <h1>Industrial Sensor Dashboard</h1>

      <form id="sensor-form">
        <label for="name">Sensor name</label>
        <input id="name" required maxlength="80"
               placeholder="e.g. Pump-01">

        <label for="temperature">Temperature</label>
        <input id="temperature" type="number"
               min="-50" max="250" step="any" required>

        <label for="status">Status</label>
        <select id="status">
          <option value="online">Online</option>
          <option value="offline">Offline</option>
        </select>

        <button type="submit">Add sensor</button>
      </form>

      <p id="message" role="status"></p>
      <button id="refresh">Refresh sensors</button>
      <ul id="sensor-list"></ul>

      <script>
        async function loadSensors() {
          const response = await fetch("/api/sensors");
          const sensors = await response.json();
          const list = document.querySelector("#sensor-list");
          list.replaceChildren();

          sensors.forEach(sensor => {
            const item = document.createElement("li");
            item.textContent =
              `${sensor.name}: ${sensor.temperature} °C (${sensor.status})`;
            list.appendChild(item);
          });
        }

        document.querySelector("#sensor-form")
          .addEventListener("submit", async event => {
            event.preventDefault();

            const response = await fetch("/api/sensors", {
              method: "POST",
              headers: {"Content-Type": "application/json"},
              body: JSON.stringify({
                name: document.querySelector("#name").value,
                temperature: Number(
                  document.querySelector("#temperature").value
                ),
                status: document.querySelector("#status").value
              })
            });

            const message = document.querySelector("#message");

            if (response.ok) {
              message.textContent = "Sensor added successfully";
              event.target.reset();
              await loadSensors();
            } else {
              const error = await response.json();
              message.textContent = error.detail
                ? JSON.stringify(error.detail)
                : "Request failed";
            }
          });

        document.querySelector("#refresh")
          .addEventListener("click", loadSensors);

        loadSensors();
      </script>
    </body>
    </html>
    """

