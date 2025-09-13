jsPlumb.ready(function() {
    jsPlumb.setContainer("sandbox");

    const sandbox = document.getElementById('sandbox');
    const blocks = document.querySelectorAll('.subsystem-block');

    const subsystemIdMap = {};
    blocks.forEach(block => {
        const blockName = block.getAttribute('data-name');
        const blockId = block.id;
        if (blockName && blockId) {
            subsystemIdMap[blockName.trim().toLowerCase()] = blockId;
        }
    });

    let familyData = { subsistemas: [] };
    const subsystemsDataAttr = sandbox.getAttribute('data-subsystems');
    if (subsystemsDataAttr) {
        try {
            familyData.subsistemas = JSON.parse(subsystemsDataAttr);
        } catch (e) {
            console.error("Erro ao analisar dados JSON de subsistemas:", e);
        }
    }

    familyData.subsistemas.forEach(function(subsystem) {
        const sourceBlockId = subsystemIdMap[subsystem.nome_subsistema.trim().toLowerCase()];

        if (!sourceBlockId) {
            console.error("ID de origem não encontrado para:", subsystem.nome_subsistema);
            return;
        }

        subsystem.produtos_saida.forEach(function(produto) {
            if (produto.fluxos && produto.fluxos.length > 0) {
                produto.fluxos.forEach(function(fluxo) {
                    if (fluxo.destino) {
                        const targetBlockId = subsystemIdMap[fluxo.destino.trim().toLowerCase()];

                        if (targetBlockId) {
                            const strokeWidth = fluxo.porcentagem ? (parseFloat(fluxo.porcentagem) / 10) + 1 : 1; 

                            jsPlumb.connect({
                                source: sourceBlockId,
                                target: targetBlockId,
                                anchors: ["AutoDefault", "AutoDefault"], 
                                connector: ["Bezier", { curviness: 80 }],
                                endpoint: "Blank", 
                                paintStyle: { stroke: "#51d360", strokeWidth: strokeWidth },
                                cssClass: "flow-connection", 
                                connectorOverlays: [
                                    ["Arrow", { width: 12, length: 12, location: 1 }],
                                    ["Label", { label: produto.nome, location: 0.5, id: "label" }]
                                ]
                            });
                        }
                    }
                });
            }
        });
    });
});