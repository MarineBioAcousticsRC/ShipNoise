function [sdBRadon0,projectionAngles,xVecResize,yVecResize] = calc_radon(shipTrack,sdB,xVec,yVec)
plotOn = 1;
%azimuthExtrap = interp1(shipTrack.dnums,shipTrack.azimuth,specTime,'pchip');
%mySpec = (flipud(sdB(1:300,:)));%floor(size(sdB,2)/2):end)));
N = 512;
B = imresize(sdB,[N,N]);
xVecResize = imresize(xVec,[1,N]);
yVecResize = imresize(yVec',[1,N]);

projectionAngles = 0:(180/(N+2)):179;
[R,xP] = radon(B,projectionAngles);
sR = sum(R == 0,1);
%[~,midPoint] = max(sR);
midPoint= N/2;

R0= R;
R0(:,[midPoint-3:midPoint+5]) = 0;
%R0(:,[1:3]) = 0;

sdBRadon0 = iradon(R0,projectionAngles,'linear','Ram-Lak');
sdBRadon = iradon(R,projectionAngles,'linear','Ram-Lak');
yMin = min(find(mean(sdBRadon,2)>10));
yMax = max(find(mean(sdBRadon,2)>10));
%sdBRadon = sdBRadon([yMin:yMax],:);


if plotOn

   
    toPlot = shipTrack.range<=6000;
    figure(12);clf
    subplot(1,3,1)
    plot(shipTrack.dnums(toPlot),shipTrack.range(toPlot)/1000)
    datetick('x','keeplimits')
    
    xlabel('Time')
    ylabel('Range (km)')
    grid on
   
    subplot(1,3,2)
    xVecResizekm = floor(xVecResize/100)/10;

    imagesc(1:512,yVecResize,sdBRadon(2:end-1,2:end-1))
    set(gca,'ydir','normal')
    set(gca,'xticklabel',(xVecResizekm(get(gca,'xtick'))))
    set(gca,'clim',[60,90])
    % set(gca,'yticklabel',floor(yVecResize(get(gca,'ytick'))))
    xlabel('Range (km)')
    ylabel('Frequency (Hz)')
    
    subplot(1,3,3)
    imagesc(1:512,yVecResize,sdBRadon0(2:end-1,2:end-1))
    set(gca,'ydir','normal')
    set(gca,'xticklabel',(xVecResizekm(get(gca,'xtick'))))
    set(gca,'clim',[60,90])
    colormap(jet)
    set(gca,'yticklabel',floor(yVecResize(get(gca,'ytick')+1)))
    xlabel('Range (km)')
%     subplot(1,4,4)
%     imagesc(flipud(B))
%     set(gca,'clim',[60,90])
%     colormap(jet)
   
    
end
