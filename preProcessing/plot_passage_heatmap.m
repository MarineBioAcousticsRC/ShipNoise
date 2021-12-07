intLat = 34100:1:34500;
intLon = (-120200):1:(-119850);

colorBox = zeros(length(intLat),length(intLon));


fList = dir('F:\MarineCadastre\matFilesMarCad\siteB_AIS_20000m_*.mat');
for iD = 1:length(fList)
    load(fullfile(fList(iD).folder,fList(iD).name))
    myLats = round(vertcat(shipTracks(:).lats)*1000)-intLat(1)+1;
    myLons = round(vertcat(shipTracks(:).lons)*1000)-intLon(1)+1;
    
    
    for iR = 1:size(myLats,1)
        
        subsIdx = sub2ind(size(colorBox),myLats(iR),myLons(iR)) ;
        colorBox(subsIdx) = colorBox(subsIdx)+1;
    end
end

siteB = [ 34.2755, -120.0185 ];

figure(10);clf

imagesc(intLon/1000,intLat/1000,log10(colorBox))
colormap(jet)
set(gca,'ydir','normal')
hold on
plot(siteB(2),siteB(1),'^k','markersize',10,'markerfacecolor','r')
xlim([-120.18,-119.87])
ylim([34.14,34.4])
set(gca,'tickdir','out')
set(gca,'clim',[0,3])
