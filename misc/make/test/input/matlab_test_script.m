rng(0)
test = rand(1)
save('../../output/matlab_test.mat')
x = 1:100;
y = x.^2;
plot(x, y)
print('-depsc', '../../output/matlab_test.eps');
exit
