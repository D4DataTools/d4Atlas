



global_markers.ptContent.forEach(content_entry => {
  if (Array.isArray(content_entry.arGlobalMarkerActors)) {
    content_entry.arGlobalMarkerActors.forEach(global_marker_actor => {
      if (global_marker_actor.snoWorld.name === 'Sanctuary_Eastern_Continent' && global_marker_actor.snoMarkerSet.name) {
        let marker_set = loadData(global_marker_actor.snoMarkerSet);
        console.log('[' + COLOR_YELLOW + 'World' + COLOR_NONE + '] Sanctuary_Eastern_Continent => [' + COLOR_YELLOW + 'MarkerSet' + COLOR_NONE + ']', global_marker_actor.snoMarkerSet.name, '=> snoMarkerSet[' + COLOR_GREEN + (Array.isArray(marker_set.tMarkerSet) && marker_set.tMarkerSet.length) + COLOR_NONE +']');
        processMarkerSet(marker_set);
      }
    });
  }
});

Sanctuary_Eastern_Continent.ptServerData.forEach(server_data => {
  server_data.arSubzones.forEach(subzone_entry => {
    let subzone = loadData(subzone_entry);

    subzone.unk_9a1125c.forEach(entry => {
      if (entry.snoMarkerSet && entry.snoMarkerSet.groupName === 'MarkerSet') {
        let marker_set = loadData(entry.snoMarkerSet);
        console.log('[' + COLOR_YELLOW + 'World' + COLOR_NONE + '] Sanctuary_Eastern_Continent => [' + COLOR_YELLOW + 'Subzone' + COLOR_NONE + ']', subzone_entry.name, '=> [' + COLOR_YELLOW + 'MarkerSet' + COLOR_NONE + ']', entry.snoMarkerSet.name, '=> snoMarkerSet[' + COLOR_GREEN + (Array.isArray(marker_set.tMarkerSet) && marker_set.tMarkerSet.length) + COLOR_NONE +']');
        processMarkerSet(marker_set);
      }
    });
  });
});