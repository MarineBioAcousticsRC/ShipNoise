[I1] = calcRadon 

azimuthExtrap = interp1(shipTracks(s).dnums,shipTracks(s).azimuth,specTime,'pchip');
mySpec = (flipud(sdB(1:300,:)));%floor(size(sdB,2)/2):end)));
R = radon(mySpec,azimuthExtrap-110);
sR = sum(R==0,1);
[~,midPoint] = max(sR);
R(:,[midPoint-1:midPoint+2]) = 0;
I1 = iradon(R,azimuthExtrap-110);


figure(10);clf
subplot(1,3,1)
imagesc(R)
subplot(1,3,2)
yMin = min(find(sum(I1,2)>0));
yMax = max(find(sum(I1,2)>0));
imagesc(I1)
set(gca,'clim',[80,130])
ylim([yMin,yMax])
subplot(1,3,3)
B = (mySpec);
imagesc(B)
set(gca,'clim',[60,105])

