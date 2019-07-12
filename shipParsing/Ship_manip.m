aug2014COP = load('J:\ShippingCINMS_data\COP_monthStack_2014-08.mat');
aug2014COP.myType = [aug2014COP.subSetData(:).shipType]';
aug2014COP.CargoIdx = find(strcmp(aug2014COP.myType,'Cargo'));
aug2014COP.CargoCount = length(aug2014COP.CargoIdx);
aug2014COP.linear = 10.^aug2014COP.imageStack;
aug2014COP.linearSpectrum = median(aug2014COP.linear,2);

plot(aug2014COP.subSetData(aug2014COP.CargoIdx).CPADist)


figure(11)
imagesc(log(median(aug2014COP.linear(:,:,aug2014COP.CargoIdx),3)))
colormap(jet)
colorbar
set(gca,'YDir','normal')
caxis([-100,-10])

jan2015COP = load('J:\ShippingCINMS_data\COP_monthStack_2015-01.mat')
jan2015COP.myType = [jan2015COP.subSetData(:).shipType]';
jan2015COP.CargoIdx = find(strcmp(jan2015COP.myType,'Cargo'));
jan2015COP.CargoCount = length(jan2015COP.CargoIdx);
jan2015COP.linear = 10.^jan2015COP.imageStack;
jan2015COP.linearSpectrum = median(jan2015COP.linear,2);
figure(22)
imagesc(log(median(jan2015COP.linear(:,:,jan2015COP.CargoIdx),3)))
colormap(jet)
colorbar
set(gca,'YDir','normal')
caxis([-100,-10])

figure(23)
plot(subSetData(1).fLog10,log10(median(jan2015COP.linearSpectrum(:,:,jan2015COP.CargoIdx),3)))
hold on
plot(subSetData(1).fLog10,log10(median(aug2014COP.linearSpectrum(:,:,aug2014COP.CargoIdx),3)))
