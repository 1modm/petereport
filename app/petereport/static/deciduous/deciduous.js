/* 
 * Adapted version of https://github.com/rpetrich/deciduous
 */


function wordwrap(text, limit) {
    text = String(text);
    if (text.indexOf("\n") != -1) {
        return text;
    }
    const split = text.split(" ");
    let all = [];
    let current = [];
    let currentLength = 0;
    for (let i = 0; i < split.length; i++) {
        const line = split[i];
        if (currentLength == 0 || (currentLength + line.length < limit && line[0] != "(")) {
            current.push(line);
            currentLength += line.length;
        } else {
            all.push(current.join(" "));
            current = [line];
            currentLength = line.length;
        }
    }
    all.push(current.join(" "));
    return all.join("\n");
}



function mangleName(name) {
    if (/^[A-Za-z]\w*$/.test(name)) {
        return name;
    }
    return JSON.stringify(name);
}



function line(name, properties) {
    const entries = Object.entries(properties);
    if (entries.length == 0) {
        return name;
    }
    return name + " [ " + entries.map(([key, value]) => `${key}=${JSON.stringify(value)}`).join(" ") + " ]";
}


function parseFrom(raw) {
    if (typeof raw == "object") {
        const [fromName, label] = Object.entries(raw)[0];
        return [fromName, label, raw]
    }
    return [String(raw), null, {}];
}


const themes = {
    "classic": {
        "edge": "#2B303A",
        "edge-text": "#DB2955",
        "backwards-edge": "#7692FF",
        "reality-fill": "#2B303A",
        "reality-text": "#FFFFFF",
        "fact-fill": "#C6CCD2",
        "attack-fill": "#ED96AC",
        "mitigation-fill": "#ABD2FA",
        "goal-fill": "#DB2955",
        "goal-text": "#FFFFFF",
    },
    "default": {
        "edge": "#2B303A",
        "edge-text": "#010065",
        "backwards-edge": "#7692FF",
        "reality-fill": "#272727",
        "reality-text": "#FFFFFF",
        "fact-fill": "#D2D5DD",
        "attack-fill": "#ffa6d5",
        "mitigation-fill": "#B9D6F2",
        "goal-fill": "#5f00c2",
        "goal-text": "#FFFFFF",
    },
}




function convertToDot(yaml) {
    const parsed = jsyaml.load(yaml);
    const font = 'Arial'
    const theme = themes[Object.hasOwnProperty.call(themes, parsed.theme) ? parsed.theme : "default"];

    const title_attacktree = document.getElementById("id_title");



    const header = `// Generated from https://swagitda.com/deciduous/
digraph {
// base graph styling
rankdir="TB";
splines=true;
overlap=false;
nodesep="0.2";
ranksep="0.4";
//label=${title_attacktree.value};
labelloc="t";
fontname=${JSON.stringify(font)};
node [ shape="plaintext" style="filled, rounded" fontname=${JSON.stringify(font)} margin=0.2 ]
edge [ fontname=${JSON.stringify(font)} fontsize=12 color="${theme["edge"]}" ]

// is reality a hologram?
reality [ label="Reality" fillcolor="${theme["reality-fill"]}" fontcolor="${theme["reality-text"]}" ]

`;
    const goals = parsed.goals || [];
    const facts = parsed.facts || [];
    const attacks = parsed.attacks || [];
    const mitigations = parsed.mitigations || [];
    const filter = parsed.filter || [];
    const subgraphs = [];
    const forwards = {};
    const forwardsAll = {};
    const backwards = {};
    const allNodes = [...facts, ...attacks, ...mitigations, ...goals];
    const types = {};
    for (const node of allNodes) {
        const [toName] = Object.entries(node)[0];
        const fromNames = backwards[toName] || (backwards[toName] = []);
        if (node.from) {
            for (const from of node.from) {
                const [fromName, label, props] = parseFrom(from);
                if (!from.backwards && !from.ungrouped) {
                    const toNames = forwards[fromName] || (forwards[fromName] = []);
                    toNames.push(toName);
                    fromNames.push(fromName);
                }
                const toNames = forwardsAll[fromName] || (forwardsAll[fromName] = []);
                toNames.push(toName);
            }
        }
    }
    function anyDominates(forwards, d, n) {
        // search to see if any nodes in d dominate n
        // nodes dominate themselves
        const search = [];
        const added = {};
        for (const other of d) {
            added[other] = true;
            search.push(other);
        }
        while ((d = search.shift()) !== undefined) {
            if (d === n) {
                return true;
            }
            const others = forwards[d];
            if (others !== undefined) {
                for (const other of others) {
                    if (!Object.hasOwnProperty.call(added, other)) {
                        added[other] = true;
                        search.push(other);
                    }
                }
            }
        }
        return false;
    }
    function shouldShow(n) {
        if (filter.length == 0 || anyDominates(forwardsAll, filter, n)) {
            return true;
        }
        const arrayN = [n];
        return filter.find(other => anyDominates(forwardsAll, arrayN, other));
    }
    function defaultLabelForName(name) {
        return name.replace(/_/g, " ").replace(/^[a-z]/, c => c.toUpperCase());
    }
    function nodes(type, values, properties) {
        const result = [];
        for (const value of values) {
            const [name, label] = Object.entries(value)[0];
            types[name] = type;
            if (shouldShow(name)) {
                result.push(line(mangleName(name), {
                    label: wordwrap(label === null ? defaultLabelForName(name) : label, 18),
                    ...properties,
                }));
            }
        }
        return result;
    }
    const allNodeLines = [
        `// facts`,
        ...nodes("fact", facts, {
            fillcolor: theme["fact-fill"],
        }),
        `// attacks`,
        ...nodes("attack", attacks, {
            fillcolor: theme["attack-fill"],
        }),
        `// mitigations`,
        ...nodes("mitigation", mitigations, {
            fillcolor: theme["mitigation-fill"],
        }),
        `// goals`,
        ...nodes("goal", goals, {
            fillcolor: theme["goal-fill"],
            fontcolor: theme["goal-text"],
        })
    ];
    function edges(entries, properties) {
        return entries.reduce((edges, value) => {
            const [name] = Object.entries(value)[0];
            if (!shouldShow(name)) {
                return edges;
            }
            (value.from || []).forEach((from) => {
                const [fromName, label, fromProps] = parseFrom(from);
                if (!shouldShow(fromName)) {
                    return;
                }
                const props = {
                    ...properties,
                };
                if (label !== null) {
                    props.xlabel = wordwrap(label, 20);
                    props.fontcolor = theme["edge-text"];
                }
                if (typeof fromProps.implemented == "boolean" && !fromProps.implemented) {
                    props.style = "dotted";
                }
                if (fromProps.backwards) {
                    props.style = "dotted";
                    props.color = theme["backwards-edge"];
                    props.weight = "0";
                }
                edges.push(line(`${mangleName(fromName)} -> ${mangleName(name)}`, props));
            });
            return edges;
        }, []);
    }
    const allEdgeLines = [...edges(goals, {}), ...edges(attacks, {}), ...edges(mitigations, {}), ...edges(facts, {})];
    const goalNames = goals.map((goal) => {
        const [goalName] = Object.entries(goal)[0];
        return goalName;
    });
    for (const [fromName, toNames] of Object.entries(forwards)) {
        if (!shouldShow(fromName)) {
            continue;
        }
        const copy = toNames.concat();
        const filteredToNames = [];
        for (let i = 0; i < toNames.length; i++) {
            copy.splice(i, 1);
            if (!anyDominates(forwards, copy, toNames[i]) && goalNames.indexOf(toNames[i]) == -1 && shouldShow(toNames[i])) {
                filteredToNames.push(toNames[i]);
            }
            copy.splice(i, 0, toNames[i]);
        }
        if (filteredToNames.length > 1) {
            subgraphs.push(`    subgraph ${mangleName(fromName)}_order {
rank=same;
${filteredToNames.map(toName => mangleName(toName) + ";").join("\n        ")}
}
${line(filteredToNames.map(mangleName).join(" -> "), { style: "invis" })}`);
        }
    }
    const shownGoals = goalNames.filter(shouldShow);
    if (shownGoals > 1) {

        subgraphs.push(`    subgraph goal_order {
rank=same;
${shownGoals.map(goalName => mangleName(goalName) + ";").join("\n        ")}
}`);
        subgraphs.push("    " + line(shownGoals.join(" -> "), { style: "invis" }));
    }
    subgraphs.push(`    { rank=min; reality; }`);
    for (const node of allNodes) {
        const [toName] = Object.entries(node)[0];
        if (shouldShow(toName) && !forwards[toName] && shownGoals.indexOf(toName) === -1) {
            for (const goalName of shownGoals) {
                subgraphs.push("    " + line(mangleName(toName) + " -> " + mangleName(goalName), { style: "invis", weight: 0 }));
            }
        }
    }
    subgraphs.push(`    { rank=max; ${shownGoals.map(goalName => mangleName(goalName) + "; ").join("")}}`);
    const footer = "\n\n}\n";
    return [header + "    " + allNodeLines.join("\n    ") + "\n\n    " + allEdgeLines.join("\n    ") + "\n\n    // subgraphs to give proper layout\n" + subgraphs.join("\n\n")  + footer, title_attacktree.value, types];
}



const renderTarget = document.getElementById("renderTarget");
const errorTarget = document.getElementById("errorTarget");
const inputSource = document.getElementById("id_attacktree");

const downloadLink = document.getElementById("downloadLink");
const downloadSvgLink = document.getElementById("downloadSvgLink");

const UpdateRenderTarget = document.getElementById("UpdateRenderTarget");
const FindingTarget = document.getElementById("id_finding");


window["@hpcc-js/wasm"].graphvizSync().then(graphviz => {
    let lastInput = "";
    let lastObjectURL = "";
    let lastSvgObjectURL = "";
    let types = {};



    function rerender() {

        const newInput = inputSource.value;

        if (newInput != lastInput) {
            lastInput = newInput;



            try {
                let dot, title;
                [dot, title, types] = convertToDot(newInput);

                document.title = `Deciduous - Security Decision Tree Generator (${title})`;
                const svg = graphviz.layout(dot, "svg", "dot");

                renderTarget.innerHTML = svg;

                const svgElement = renderTarget.querySelector("svg");

                if (svgElement) {
                    const scale = 0.75;
                    svgElement.setAttribute("width", parseInt(svgElement.getAttribute("width"), 10) * scale + "pt");
                    svgElement.setAttribute("height", parseInt(svgElement.getAttribute("height"), 10) * scale + "pt");
                }


                // Create a download link
                if (window.File && URL.createObjectURL) {
                    // DOT
                    const file = new File([dot], "graph.dot", {
                        "type": "text/vnd.graphviz",
                    });
                    downloadLink.download = title + ".dot";
                    const newObjectURL = URL.createObjectURL(file);
                    downloadLink.href = newObjectURL;
                    if (lastObjectURL != "") {
                        URL.revokeObjectURL(lastObjectURL);
                    }
                    lastObjectURL = newObjectURL;

                    // SVG
                    const svgFile = new File([svg], "graph.svg", {
                        "type": "image/svg+xml",
                    });
                    downloadSvgLink.download = title + ".svg";
                    const newSvgObjectURL = URL.createObjectURL(svgFile);
                    downloadSvgLink.href = newSvgObjectURL;
                    if (lastSvgObjectURL != "") {
                        URL.revokeObjectURL(lastSvgObjectURL);
                    }
                    lastSvgObjectURL = newSvgObjectURL;
                }


                // Add quick linky links
                for (const title of renderTarget.querySelectorAll("title")) {
                    title.parentNode.style.cursor = "pointer";
                    title.parentNode.addEventListener("click", () => {
                        const node = title.textContent;
                        const index = lastInput.indexOf("\n- " + node);
                        if (index != -1) {
                            inputSource.blur();
                            inputSource.selectionEnd = inputSource.selectionStart = index + 3;
                            inputSource.focus();
                            inputSource.selectionEnd = index + 3 + node.length;

                        }
                    }, false);
                }

                // Clear any error text
                errorTarget.innerText = "";
            } catch (e) {
                errorTarget.innerText = String(e);
            }
        }
    }


    function updateImage(){

        const newInput = inputSource.value;

            try {
                let dot, title;
                [dot, title, types] = convertToDot(newInput);

                document.title = `Deciduous - Security Decision Tree Generator (${title})`;
                const svg = graphviz.layout(dot, "svg", "dot");

                renderTarget.innerHTML = svg;

                const svgElement = renderTarget.querySelector("svg");

                if (svgElement) {
                    const scale = 0.75;
                    svgElement.setAttribute("width", parseInt(svgElement.getAttribute("width"), 10) * scale + "pt");
                    svgElement.setAttribute("height", parseInt(svgElement.getAttribute("height"), 10) * scale + "pt");

                    document.getElementById("id_svg_file").value = svg;
                }

                // Clear any error text
                errorTarget.innerText = "";
            } catch (e) {
                errorTarget.innerText = String(e);
            }
        
        rerender();
    }



    inputSource.addEventListener("change", rerender, false);
    inputSource.addEventListener("input", rerender, false);

    UpdateRenderTarget.addEventListener("click", updateImage, false);

    rerender();

});