import globalStateManager from "./globalState.js";
import oldManGlobalStateManager from "./oldManGlobaleState.js";
import playerGlobalStateManager from "./playerGlobalState.js";

export const oldManState = oldManGlobalStateManager().getInstance();
export const playerState = playerGlobalStateManager().getInstance();
export const gameState = globalStateManager().getInstance();