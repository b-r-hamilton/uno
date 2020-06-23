path = 'C:\Users\bydd1\Downloads\file.xlsx';
data1 = xlsread(path);
x = data1(:, 1); %meander wavelength 
y = data1(:, 3); %discharge 
modelfun = @(b,x)((x./b(1)).^(1/b(2)));
opts = statset('nlinfit');
pts.RobustWgtFun = 'bisquare';
beta0 = [30;0.5];
[beta, R, J, CovB, MSE] = nlinfit(x, y, modelfun, beta0, opts);
disp(beta)

path = 'C:\Users\bydd1\Downloads\meandwave_for_brynn.csv';
data2 = readmatrix(path);
testx = data2(:, 2); %reconstructed meander wavelengths 

[ypred,delta] = nlpredci(modelfun,testx,beta,R,'Covar',CovB,'MSE',MSE,'SimOpt','on');
lower = ypred - delta;
upper = ypred + delta;

[ypred2,delta2] = nlpredci(modelfun,testx,beta,R,'Covar', CovB, 'MSE', MSE, 'SimOpt', 'on', 'alpha', 1-0.68)
lower2 = ypred2 - delta2;
upper2 = ypred2 + delta2;

%%
figure()
ages = data2(:, 1);

plot(ages, ypred, 'k')
hold('on')

plot(ages, upper, 'r--')
plot(ages, lower, 'r--')
plot(ages, upper2, 'g--', 'LineWidth', 1)
plot(ages, lower2, 'g--', 'LineWidth', 1)
xlabel('time (years)')
ylabel('discharge')
title('reconstructed discharge')


%%
figure()
plot(x,y, 'ko')
x = sort(x);
[ypred,delta] = nlpredci(modelfun,x,beta,R,'Covar',CovB,'MSE',MSE,'SimOpt','on');
lower = ypred - delta;
upper = ypred + delta;

[ypred2,delta2] = nlpredci(modelfun,x,beta,R,'Covar', CovB, 'MSE', MSE, 'SimOpt', 'on', 'alpha', 1-0.68)
lower2 = ypred2 - delta2;
upper2 = ypred2 + delta2;

hold('on')

plot(x, upper, 'r--','LineWidth',1.5)
plot(x, lower, 'r--','LineWidth',1.5)
plot(x, ypred, 'k', 'LineWidth', 2)
plot(x, upper2, 'g--', 'LineWidth', 1)
plot(x, lower2, 'g--', 'LineWidth', 1)
xlabel('meander wavelength (m)')
ylabel('discharge (cms)')
title('Nonlinear regression of discharge as a function of wavelength')