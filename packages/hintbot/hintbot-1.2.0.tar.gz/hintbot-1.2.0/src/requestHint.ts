import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { NotebookPanel } from '@jupyterlab/notebook';
import { Dialog, showDialog } from '@jupyterlab/apputils';
import { IJupyterLabPioneer } from 'jupyterlab-pioneer';
import { showReflectionDialog } from './showReflectionDialog';
import { createHintBanner } from './createHintBanner';
import { ICellModel } from '@jupyterlab/cells';
import { requestAPI } from './handler';

export const requestHint = async (
  notebookPanel: NotebookPanel,
  settings: ISettingRegistry.ISettings,
  pioneer: IJupyterLabPioneer,
  cell: ICellModel
  // hintType: string
) => {
  const gradeId = cell.getMetadata('nbgrader')?.grade_id;
  const remainingHints = cell.getMetadata('remaining_hints');

  if (document.getElementById('hint-banner')) {
    showDialog({
      title: 'Please review previous hint first.',
      buttons: [
        Dialog.createButton({
          label: 'Dismiss',
          className: 'jp-Dialog-button jp-mod-reject jp-mod-styled'
        })
      ]
    });
    pioneer.exporters.forEach(exporter => {
      pioneer.publishEvent(
        notebookPanel,
        {
          eventName: 'HintAlreadyExists',
          eventTime: Date.now(),
          eventInfo: {
            gradeId: gradeId
          }
        },
        exporter,
        false
      );
    });
  } else if (remainingHints < 1) {
    showDialog({
      title: 'No hint left for this question.',
      buttons: [
        Dialog.createButton({
          label: 'Dismiss',
          className: 'jp-Dialog-button jp-mod-reject jp-mod-styled'
        })
      ]
    });
    pioneer.exporters.forEach(exporter => {
      pioneer.publishEvent(
        notebookPanel,
        {
          eventName: 'NotEnoughHint',
          eventTime: Date.now(),
          eventInfo: {
            gradeId: gradeId
          }
        },
        exporter,
        false
      );
    });
  } else {
    let preReflection = settings.get('preReflection').composite as boolean;
    let postReflection = settings.get('postReflection').composite as boolean;

    try {
      const id: string = await requestAPI('id');
      const n =
        id
          .split('')
          .map(c => c.charCodeAt(0) - 64)
          .reduce((acc, val) => acc + val, 0) % 3;
      console.log(`Condition ${n}`);

      if (n === 0) {
        preReflection = true;
        postReflection = false;
      } else if (n === 1) {
        preReflection = false;
        postReflection = true;
      } else {
        preReflection = false;
        postReflection = false;
      }
    } catch (e) {
      pioneer.exporters.forEach(exporter => {
        pioneer.publishEvent(
          notebookPanel,
          {
            eventName: 'ConvertIDError',
            eventTime: Date.now(),
            eventInfo: {
              error: e
            }
          },
          exporter,
          true
        );
      });
      console.log(e);
    }

    createHintBanner(notebookPanel, pioneer, cell, postReflection);

    cell.setMetadata('remaining_hints', remainingHints - 1);
    document.getElementById(gradeId).innerText = `Hint (${
      remainingHints - 1
    } left for this question)`;
    notebookPanel.context.save();

    if (preReflection) {
      document.getElementById('hint-banner').style.filter = 'blur(10px)';

      const dialogResult = await showReflectionDialog(
        'Write a brief statement of what the problem is that you are facing and why you think your solution is not working.'
      );
      document.getElementById('hint-banner').style.filter = 'none';

      pioneer.exporters.forEach(exporter => {
        pioneer.publishEvent(
          notebookPanel,
          {
            eventName: 'PreReflection',
            eventTime: Date.now(),
            eventInfo: {
              status: dialogResult.button.label,
              gradeId: gradeId,
              reflection: dialogResult.value
              // hintType: hintType
            }
          },
          exporter,
          true
        );
      });
      if (dialogResult.button.label === 'Cancel') {
        await requestAPI('cancel', {
          method: 'POST',
          body: JSON.stringify({
            problem_id: gradeId
          })
        });
      }
    }
  }
};
