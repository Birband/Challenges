import React, { useState, useEffect, useRef } from "react";
import Graph  from "react-vis-network-graph";
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
  const [selectedNode, setSelectedNode] = useState<number | null>(null);
  const [graphKey, setGraphKey] = useState(uuidv4());
  const [size, setSize] = useState({ width: 0, height: 0 });
  const canvasRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleResize = () => {
      if (canvasRef.current) {
        setSize({
          width: canvasRef.current.clientWidth,
          height: canvasRef.current.clientHeight,
        });
      }
    };

    window.addEventListener("resize", handleResize);
    handleResize();

    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);


  const addNode = () => {
    const newId = nodes.length > 0 ? Math.max(...nodes.map(n => n.id)) + 1 : 1;
    setNodes([...nodes, { id: newId, label: `Node ${newId}` }]);
    if (nodes.length > 0) {
      setEdges([...edges, { from: nodes[nodes.length - 1].id, to: newId }]);
    }
    setGraphKey(uuidv4());
  };

  const onSelectNode = (event: any) => {
    setSelectedNode(event.nodes[0]);
  }

  return (
    <>
    <div ref={canvasRef} id="canvas">
      <Graph
        key={graphKey}
        graph={{ nodes, edges }}
        options={{
          autoResize: true,
          height: `${size.height}px`,
          width: `${size.width}px`,
          nodes: { shape: "circle" },
        }}
        events={{
          select: onSelectNode,
        }}
      />
    </div>
    <div id="sidebar">
      <h2>Selected Node</h2>
      <p>{selectedNode ? `Node ${selectedNode}` : "None"}</p>
      <h2>Actions</h2>
      <button onClick={addNode}>Add Node</button>
    </div>
    </>
  );
};

export default GraphComponent;
