# HSR Visualisation

Just some visualisations for weaknesses in Honkai: Star Rail, it ain't much but it's honest work.

### Visualisations
All charts for current content (1.0) are [available here](/charts/)
Charts follow the nomenclature `name-mob_type_mode-planet_mode`. `name` being either `mobs_per_weakness_x` or `weaknesses_overlap`.
Configuration is as follow:
```json
planet_modes = {
    "every planets": ["Herta Space Station", "Jarilo-VI", "The Xianzhou Luofu", "Simulated Universe"],
    "Herta Space Station": ["Herta Space Station"],
    "Jarilo-VI": ["Jarilo-VI"], 
    "The Xianzhou Luofu": ["The Xianzhou Luofu"]
}

mob_type_modes = {
    "all": ["Normal","Elite","Boss", "Boss' Invocation"],
    "normal": ["Normal"],
    "elite": ["Elite","Boss", "Boss' Invocation"]
}
```
Zone declaration [available here](zones.json).

### Data
Data [available here](mobs.json), some notes on the data:
- no distinction between "Final Boss" and "Boss", like Gepard, Bronya, Svarog are considered boss the same way Cocolia is.
- distinction between elite and bosses
- Each trotter is considered elite, the reason being warp trotter is a unique unit: once you kill it, it doesn't respawn.
- Svarog's, Cocolia and Abundant Ebon Deer's invocations weren't counted previously, I added them and considered them as boss invocation on the same region
- The "Elite chart" refer to Elite, Boss and Boss' invocation. 
- The "Doomsday Beast" wasn't counted previously, it is now but I didn't add the invocation since the fight is a bit special.
- Some fragmentum monsters appears on several planets.