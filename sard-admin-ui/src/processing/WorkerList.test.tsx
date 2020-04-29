import { render, wait } from '@testing-library/react';
import { WorkerList } from './WorkerList';

test('GroupView renders', async () => {
  const { baseElement, getByText } = render(WorkerList({
    isLocked: () => true,
    isRunning: () => true,
    workers: [
      {
        host_ip: '1.2.3.4',
        pod_ip: '5.6.7.8',
        image: 'asfd/worker:1234',
        name: 'ipedworker-298347',
        node_name: 'sardcloudXX',
        ready: false,
        evidence: '/ops/A/B/imagem.dd',
        processed: 91084.0,
        found: 92494.0,
      }
    ]
  }));
  await wait(() => {
    expect(baseElement).toBeDefined()
  })
  const item = getByText(/sardcloudXX/)
  expect(item.textContent.trim()).toEqual('+ sardcloudXX - /ops/A/B/imagem.dd - running -  locked - 91084/92494')
  item.click()
  expect(item.textContent.trim()).toEqual('- sardcloudXX - /ops/A/B/imagem.dd - running -  locked - 91084/92494 Host name: sardcloudXX  Host IP: 1.2.3.4  Image: asfd/worker:1234  Pod name: ipedworker-298347  Pod IP: 5.6.7.8  Ready: false  Evidence: /ops/A/B/imagem.dd  Progress: 91084/92494')
});
