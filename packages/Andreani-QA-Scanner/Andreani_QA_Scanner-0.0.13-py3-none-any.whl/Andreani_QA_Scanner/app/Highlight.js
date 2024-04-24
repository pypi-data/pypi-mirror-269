highlight = (expression, typeElement, scroll) => {
  /**
  * Convierte la expresion en un elemento web y lo señala en pantalla.
  * @param {string} expression - xpath o queryselector que representa un objeto web.
  * @param {string} typeElement - indica si es un xpath o un queryselector.
  * @param {bool} scroll - Indica si debe scrollear la pantalla antes de señalar el elemento.
  * @returns {bool} Retorna si pudo o no señalar el elemento.
  **/
  try {
    let elementTarget, colorBox;
    if (typeElement === 'XPATH') {
      elementTarget = document.evaluate(expression, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
      colorBox = 'green';
    } else if (typeElement === 'CSS') {
      elementTarget = document.querySelector(expression);
      colorBox = 'red';
    }

    if (elementTarget) {
      if (scroll === true) {
        elementTarget.scrollIntoView({
          behavior: 'auto',
          block: 'end',
        });
      }
      const box = document.createElement('div');
      box.classList.add('box');
      document.body.appendChild(box);
      const elementTargetRect = elementTarget.getClientRects()[0];
      box.style.left = `${elementTargetRect.left}px`;
      box.style.top = `${elementTargetRect.top}px`;
      box.style.width = `${elementTargetRect.width}px`;
      box.style.height = `${elementTargetRect.height}px`;
      const style = document.createElement('style');
      style.textContent = `
        .box {
          position: absolute;
          z-index: 9999 !important;
          background-color: None;
          border: 3px solid ${colorBox};
          animation: titilar 1s infinite;
        }

        @keyframes titilar {
          0% {
            opacity: 1;
          }
          50% {
            opacity: 0.5;
          }
          100% {
            opacity: 1;
          }
        }
      `;
      document.head.appendChild(style);
      setTimeout(() => {
        document.body.removeChild(box);
        document.head.removeChild(style);
      }, 3000);
    } else {
      console.log('No es posible señalar ' + expression);
      return false;
    }
  } catch (error) {
    console.error(error);
    console.log('Error en la expresion xpath ' + expression);
    return false;
  }
  return true;
};
