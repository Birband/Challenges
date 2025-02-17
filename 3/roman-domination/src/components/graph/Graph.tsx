import React, { useState } from "react";
import Graph from "react-vis-network-graph";
import { v4 as uuidv4 } from "uuid";
import './Graph.css';

const GraphComponent: React.FC = () => {
  const [nodes, setNodes] = useState([
    { id: 1, label: "Node 1" },
    { id: 2, label: "Node 2" },
  ]);

  const [edges, setEdges] = useState([
    { from: 1, to: 2 },
  ]);

  const [graphKey, setGraphKey] = useState(uuidv4());

  const addNode = () => {
    const newId = nodes.length > 0 ? Math.max(...nodes.map(n => n.id)) + 1 : 1;
    setNodes([...nodes, { id: newId, label: `Node ${newId}` }]);
    if (nodes.length > 0) {
      setEdges([...edges, { from: nodes[nodes.length - 1].id, to: newId }]);
    }
    setGraphKey(uuidv4());
  };

  return (
    <div>
      <button onClick={addNode}>Add Node</button>
      <Graph
        key={graphKey}
        graph={{ nodes, edges }}
        options={{
          autoResize: true,
          height: "400px",
          width: "600px",
          nodes: { shape: "circle" },
        }}
      />
    </div>
  );
};

export default GraphComponent;
