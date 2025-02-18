import React, { useState, useRef } from "react";
// @ts-ignore
import Graph  from "react-vis-network-graph";
import { v4 as uuidv4 } from "uuid";
import './Graph.css';

const GraphComponent: React.FC = () => {
  // Pczątkowy graf
  const [nodes, setNodes] = useState([
    { id: 1, label: " 1 ", x: 100, y: 100 },
    { id: 2, label: " 2 ", x: 200, y: 200 }
  ]);
  const [edges, setEdges] = useState([{ from: 1, to: 2 },]);

  const [selectedNode, setSelectedNode] = useState<number | null>(null);
  const [graphKey, setGraphKey] = useState(uuidv4());
  const [toggleAddEdge, setToggleAddEdge] = useState(false);
  const canvasRef = useRef<HTMLDivElement>(null);

  const addNode = () => {
    const newId = nodes.length > 0 ? Math.max(...nodes.map(n => n.id)) + 1 : 1;
    if (!selectedNode) {
      setNodes([...nodes, { id: newId, label: ` ${newId} `, x: 100, y: 100 }]);
    } else {
      console.log(nodes)
      setNodes([...nodes, { id: newId, label: ` ${newId} `, x: nodes.find(n => n.id === selectedNode)!.x + 50, y: nodes.find(n => n.id === selectedNode)!.y + 50 }]);
    }

    if (selectedNode) {
      console.log(selectedNode);
      setEdges([...edges, { from: selectedNode, to: newId }]);
    }

    setGraphKey(uuidv4()); // to jest takie XD
  };

  const removeNode = () => {
    if (selectedNode) {
      setNodes(nodes.filter(n => n.id !== selectedNode));
      setEdges(edges.filter(e => e.from !== selectedNode && e.to !== selectedNode));
      setSelectedNode(null);

      setGraphKey(uuidv4()); // to jest takie XD
    }
  }

  const onDragEnd = (event: any) => {
    const newNodes = nodes.map(n => {
      const draggedNode = event.nodes.find((node: number) => node === n.id);
      if (draggedNode) {
        return {
          ...n,
          x: event.pointer.canvas.x,
          y: event.pointer.canvas.y
        };
      }
      return n;
    });

    setNodes(newNodes);
    setGraphKey(uuidv4()); // to jest takie XD
  }

  const onSelectNode = (event: any) => {
    if (toggleAddEdge) {
      if (selectedNode) {
        const edgeExists = edges.some(e => (e.from === selectedNode && e.to === event.nodes[0]) 
                                        || (e.from === event.nodes[0] && e.to === selectedNode));
        if (!edgeExists)
          setEdges([...edges, { from: selectedNode, to: event.nodes[0] }]);
        else {
          setEdges(edges.filter(e => (e.from !== selectedNode || e.to !== event.nodes[0]) 
                                  && (e.from !== event.nodes[0] || e.to !== selectedNode)));
        }
      }
      setGraphKey(uuidv4()); // to jest takie XD
    }
    setSelectedNode(event.nodes[0]);
    setToggleAddEdge(false);
  }

  // :)))))))))))))))))))))
  const domination = () => {
    let dominated = new Set();
    let dominationSet = new Set();
  
    let nodeDegrees = nodes.map(node => ({
      id: node.id,
      degree: edges.filter(e => e.from === node.id || e.to === node.id).length
    })).sort((a, b) => b.degree - a.degree);
  
    for (let node of nodeDegrees) {
      if (!dominated.has(node.id)) {
        dominationSet.add(node.id);
        dominated.add(node.id);
  
        edges.forEach(edge => {
          if (edge.from === node.id) dominated.add(edge.to);
          if (edge.to === node.id) dominated.add(edge.from);
        });
  
        if (dominated.size === nodes.length) break;
      }
    }
  
    const newNodes = nodes.map(n => ({
      ...n,
      label: dominationSet.has(n.id) ? ` ${n.id} ` : n.label,
      color: dominationSet.has(n.id) ? "#e63946" : undefined
    }));
  
    setNodes(newNodes);
    setGraphKey(uuidv4()); // to jest takie XD
  }

  return (
    <>
    <div ref={canvasRef} id="canvas">
      <Graph
      key={graphKey}
      graph={{ nodes, edges }}
      options={{
        autoResize: true,
        nodes: {
          size: 30,
          shape: "circle",
          borderWidth: 3,
          color: {
            border: "#1d3557",
            background: "#457b9d",
            highlight: {
              border: "#457b9d",
              background: "#1d3557",
            }
        },
        shadow: true,
        font: { 
          color: "#f1faee",
          size: 20
         }
        },
        edges: { color: "#1d3557", width: 2, arrows: { to: { enabled: false} } },
        layout: { hierarchical: false },
        physics: { enabled: false },
      }}
      events={{
        select: onSelectNode,
        dragStart: onSelectNode,
        dragEnd: onDragEnd
      }}
      />
    </div>
    <div id="sidebar">
      <h2>Selected Node</h2>
      <p>{selectedNode ? `Node ${selectedNode}` : "None"}</p>
      <h2>Actions</h2>
      <div id="actions">
      <button onClick={addNode}>Add Node</button>
      <button disabled={!selectedNode} onClick={removeNode}>Remove Node</button>
      <button disabled={!selectedNode} onClick={() => setToggleAddEdge(!toggleAddEdge)}>{toggleAddEdge ? "Disable" : "Enable"} Edge Mode</button>
      <button onClick={domination}>Dominate!</button>
      <button disabled={true}>Dominate Rome! #TODO</button> {/* TODO */}
      </div>
    </div>
    </>
  );
};

export default GraphComponent;
