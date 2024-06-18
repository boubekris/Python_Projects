import { colorizeBackground, drawBoundaries, drawTiles, fetchMapData, playAnimIfNotPlaying } from "../../utils.js";
import { generatePlayerComponents, setPlayerMovement } from "../entities/player.js";
import { generateOldManComponents, startInteraction } from "../entities/oldman.js";
import { healthBar } from "./../uiComponents/healthbar.js";
import { gameState } from "../state/stateManager.js";

export default async function house(k) {
    colorizeBackground(k, 27, 29, 52);
    const mapData = await fetchMapData("./assets/maps/house.json");

    const map = k.add([k.pos(520, 65)]);
    
    const entities = {
        oldman : null,
        player : null,
    };

    const layers = mapData.layers;

    for (const layer of layers){
        if (layer.name === "Boundaries") {
            drawBoundaries(k, map, layer);
            continue;
        }
        if (layer.name === "SpawnPoints") {
            for(const object of layer.objects) {
                if(object.name === "player") {
                    entities.player = map.add(
                        generatePlayerComponents(k, k.vec2(object.x, object.y))
                      );
                      continue;
                }
                if(object.name === "oldman") {
                    entities.oldman = map.add(
                        generateOldManComponents(k, k.vec2(object.x, object.y))
                      );
                      continue;
                }
            }
        }
        
        drawTiles(k, map, layer, mapData.tileheight, mapData.tilewidth);
    }
    k.camScale(2.75);

    setPlayerMovement(k, entities.player);
    entities.player.onCollide("door-exit", () => {
        gameState.setPreviousScene("house");
        k.go("world");
    });
    entities.player.onCollide("oldman", () => {
        startInteraction(k, entities.oldman, entities.player);
    });
    entities.player.onCollideEnd("oldman", () => {
        playAnimIfNotPlaying(entities.oldman, "oldman-down")
    });

    healthBar(k);

}