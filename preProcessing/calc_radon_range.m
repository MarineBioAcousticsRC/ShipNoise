function [sdBRadon,projectionAngles] = calc_radon_range(shipTrack,sdB,specRange,cpaIdx)
plotOn = 1;
azimuthExtrap = interp1(shipTrack.range(cpaIdx:end),shipTrack.azimuth(cpaIdx:end),specRange,'pchip');
mySpec = flipud(sdB(:,1:300)');%floor(size(sdB,2)/2):end)));
B = imresize(mySpec,[500,500]);
projectionAngles = 1:(180/502):180;
[R,xP] = radon(B,projectionAngles);
sR = sum(R==0,1);
[~,midPoint] = max(sR);
%R(:,1) = 0;
sdBRadon = iradon(R,[],'linear','Ram-Lak',1,500);
%     yMin = min(find(mean(sdBRadon,2)>10));
%     yMax = max(find(mean(sdBRadon,2)>10));
%sdBRadon = sdBRadon([yMin:yMax],:);
    
if plotOn
    figure(10);clf
    subplot(1,3,1)
    imagesc(R)
    subplot(1,3,2)

    imagesc(sdBRadon)
    %set(gca,'clim',[40,130])
%    ylim([yMin,yMax])
    subplot(1,3,3)
    B = (mySpec);
    imagesc(B)
    set(gca,'clim',[60,105])
    colormap(jet)
end
